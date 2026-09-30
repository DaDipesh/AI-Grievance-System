from datetime import datetime, timezone
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from app.services.email_service import (
    email_event_for_status_transition,
    send_complaint_notification,
    smtp_configuration_ready,
    smtp_server_label,
)


def brevo_settings(**overrides):
    """Settings shaped like a filled-in Brevo `SMTP_*` block in backend/.env."""
    settings = {
        "smtp_host": "smtp-relay.brevo.com",
        "smtp_port": 587,
        "smtp_user": "brevo-smtp-login",
        "smtp_pass": "xsmtpsib-key",
        "smtp_from": "verified.sender@example.test",
        "smtp_from_name": "AI Grievance Management System",
        "smtp_secure": False,
    }
    settings.update(overrides)
    return SimpleNamespace(**settings)


class EmailNotificationTests(unittest.TestCase):
    def setUp(self):
        self.settings = brevo_settings()
        self.smtp_patch = patch("app.services.email_service.smtplib.SMTP")
        self.smtp_class = self.smtp_patch.start()
        self.addCleanup(self.smtp_patch.stop)
        self.smtp = self.smtp_class.return_value.__enter__.return_value
        self.ssl_patch = patch("app.services.email_service.smtplib.SMTP_SSL")
        self.ssl_class = self.ssl_patch.start()
        self.addCleanup(self.ssl_patch.stop)
        self.ssl = self.ssl_class.return_value.__enter__.return_value

    def send(self, event, previous_status=None, settings=None):
        with patch("app.services.email_service.get_settings", return_value=settings or self.settings):
            send_complaint_notification(
                event,
                "citizen@example.test",
                "Asha Citizen",
                "GRV-1025",
                "Water supply is unavailable in my area.",
                occurred_at=datetime(2026, 9, 30, 10, 30, tzinfo=timezone.utc),
                previous_status=previous_status,
            )
        used = self.ssl if self.ssl.send_message.called else self.smtp
        return used.send_message.call_args.args[0]

    def test_submitted_email(self):
        email = self.send("submitted")
        self.assertEqual(email["Subject"], "Grievance GRV-1025 Submitted Successfully")
        self.assertEqual(email["From"], "AI Grievance Management System <verified.sender@example.test>")
        self.assertEqual(email["To"], "citizen@example.test")
        body = email.get_content()
        for expected in ("Asha Citizen", "GRV-1025", "Water supply is unavailable", "Status: SUBMITTED", "Submission date/time:"):
            self.assertIn(expected, body)
        self.smtp_class.assert_called_once_with("smtp-relay.brevo.com", 587, timeout=10)
        self.smtp.starttls.assert_called_once()
        self.smtp.login.assert_called_once_with(self.settings.smtp_user, self.settings.smtp_pass)
        self.smtp.send_message.assert_called_once()

    def test_in_progress_email_includes_previous_status(self):
        email = self.send("in_progress", previous_status="pending")
        self.assertEqual(email["Subject"], "Grievance GRV-1025 Is Now In Progress")
        body = email.get_content()
        self.assertIn("Previous status: PENDING", body)
        self.assertIn("Current status: IN_PROGRESS", body)
        self.assertIn("Water supply is unavailable", body)

    def test_resolved_email(self):
        email = self.send("resolved")
        self.assertEqual(email["Subject"], "Grievance GRV-1025 Has Been Resolved")
        body = email.get_content()
        self.assertIn("Status: RESOLVED", body)
        self.assertIn("Resolution date/time:", body)
        self.assertIn("Asha Citizen", body)

    def test_implicit_tls_port_uses_ssl_connection(self):
        self.send("submitted", settings=brevo_settings(smtp_port=465, smtp_secure=True))
        self.ssl_class.assert_called_once_with("smtp-relay.brevo.com", 465, timeout=10)
        self.smtp_class.assert_not_called()
        self.ssl.login.assert_called_once_with("brevo-smtp-login", "xsmtpsib-key")
        self.ssl.send_message.assert_called_once()

    def test_relay_without_starttls_is_refused_before_sending_credentials(self):
        self.smtp.has_extn.return_value = False
        with patch("app.services.email_service.get_settings", return_value=self.settings):
            with self.assertLogs("grievance.email", level="ERROR") as captured:
                send_complaint_notification("submitted", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.smtp.login.assert_not_called()
        self.smtp.send_message.assert_not_called()
        self.smtp.starttls.assert_not_called()
        self.assertTrue(any("SMTPNotSupportedError" in line for line in captured.output))

    def test_only_new_in_progress_or_resolved_transitions_trigger_email(self):
        cases = (
            ("pending", "in_progress", "in_progress"),
            ("assigned", "in_progress", "in_progress"),
            ("in_progress", "in_progress", None),
            ("in_progress", "resolved", "resolved"),
            ("resolved", "resolved", None),
            ("pending", "rejected", None),
            ("pending", "closed", None),
            (None, "submitted", None),
        )
        for old, new, expected in cases:
            with self.subTest(old=old, new=new):
                self.assertEqual(email_event_for_status_transition(old, new), expected)

    def test_other_events_do_not_send_email(self):
        with patch("app.services.email_service.get_settings", return_value=self.settings):
            send_complaint_notification("assigned", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.smtp_class.assert_not_called()

    def test_smtp_failure_is_logged_and_swallowed_without_logging_error_text(self):
        self.smtp.send_message.side_effect = OSError("secret-value-must-not-appear")
        with patch("app.services.email_service.get_settings", return_value=self.settings):
            with self.assertLogs("grievance.email", level="ERROR") as captured:
                send_complaint_notification("submitted", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.assertTrue(any("Email notification failed" in line for line in captured.output))
        self.assertNotIn("secret-value-must-not-appear", "\n".join(captured.output))

    def test_half_filled_smtp_login_skips_delivery(self):
        incomplete = brevo_settings(smtp_pass="")
        with patch("app.services.email_service.get_settings", return_value=incomplete):
            with self.assertLogs("grievance.email", level="WARNING"):
                send_complaint_notification("resolved", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.smtp_class.assert_not_called()

    def test_relay_without_credentials_is_still_attempted(self):
        # A local relay on port 1025 accepts unauthenticated mail; the parity check
        # must not block it, and login must simply be skipped.
        local = brevo_settings(smtp_host="127.0.0.1", smtp_port=1025, smtp_user="", smtp_pass="", smtp_from="dev@example.test")
        self.assertTrue(smtp_configuration_ready(local))
        with patch("app.services.email_service.get_settings", return_value=local):
            send_complaint_notification("resolved", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.smtp.login.assert_not_called()
        self.smtp.send_message.assert_called_once()

    def test_missing_sender_address_skips_delivery(self):
        with patch("app.services.email_service.get_settings", return_value=brevo_settings(smtp_from="")):
            with self.assertLogs("grievance.email", level="WARNING"):
                send_complaint_notification("resolved", "citizen@example.test", "Asha", "GRV-1025", "Complaint")
        self.smtp_class.assert_not_called()

    def test_citizen_without_email_address_skips_delivery(self):
        with patch("app.services.email_service.get_settings", return_value=self.settings):
            with self.assertLogs("grievance.email", level="WARNING"):
                send_complaint_notification("submitted", None, "Asha", "GRV-1025", "Complaint")
        self.smtp_class.assert_not_called()

    def test_configuration_readiness_and_server_label_never_expose_secrets(self):
        self.assertTrue(smtp_configuration_ready(self.settings))
        self.assertEqual(smtp_server_label(self.settings), "smtp-relay.brevo.com:587")
        self.assertFalse(smtp_configuration_ready(brevo_settings(smtp_user="")))
        self.assertFalse(smtp_configuration_ready(brevo_settings(smtp_pass="")))
        self.assertFalse(smtp_configuration_ready(brevo_settings(smtp_host="")))
        self.assertFalse(smtp_configuration_ready(brevo_settings(smtp_from="")))
        self.assertEqual(smtp_server_label(brevo_settings(smtp_pass="")), "not configured")
        self.assertNotIn("xsmtpsib-key", smtp_server_label(self.settings))


if __name__ == "__main__":
    unittest.main()
