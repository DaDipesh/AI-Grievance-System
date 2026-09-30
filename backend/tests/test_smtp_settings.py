import unittest
from unittest.mock import patch

from app.config import Settings

BREVO_ENV = {
    "SMTP_HOST": "smtp-relay.brevo.com",
    "SMTP_PORT": "587",
    "SMTP_USER": "brevo-smtp-login",
    "SMTP_PASS": "xsmtpsib-key",
    "SMTP_FROM": "verified.sender@example.test",
}


def load_settings(env):
    with patch.dict("os.environ", env, clear=True):
        # _env_file=None keeps the developer's local backend/.env out of this check.
        return Settings(_env_file=None)


class SmtpSettingsTests(unittest.TestCase):
    def test_brevo_variables_are_read_into_smtp_settings(self):
        settings = load_settings(BREVO_ENV)
        self.assertEqual(settings.smtp_host, "smtp-relay.brevo.com")
        self.assertEqual(settings.smtp_port, 587)
        self.assertEqual(settings.smtp_user, "brevo-smtp-login")
        self.assertEqual(settings.smtp_pass, "xsmtpsib-key")
        self.assertEqual(settings.smtp_from, "verified.sender@example.test")

    def test_defaults_target_the_brevo_relay_with_starttls(self):
        settings = load_settings({})
        self.assertEqual(settings.smtp_host, "smtp-relay.brevo.com")
        self.assertEqual(settings.smtp_port, 587)
        self.assertFalse(settings.smtp_secure)
        self.assertEqual(settings.smtp_user, "")
        self.assertEqual(settings.smtp_pass, "")
        self.assertEqual(settings.smtp_from, "")

    def test_sender_name_and_secure_transport_are_configurable(self):
        settings = load_settings({**BREVO_ENV, "SMTP_FROM_NAME": "Nivaran", "SMTP_SECURE": "true", "SMTP_PORT": "465"})
        self.assertEqual(settings.smtp_from_name, "Nivaran")
        self.assertTrue(settings.smtp_secure)
        self.assertEqual(settings.smtp_port, 465)

    def test_legacy_variable_names_still_work(self):
        settings = load_settings({
            "SMTP_HOST": "smtp.gmail.com",
            "SMTP_PORT": "587",
            "SMTP_USERNAME": "legacy-user",
            "SMTP_PASSWORD": "legacy-pass",
            "SMTP_FROM_EMAIL": "legacy.sender@example.test",
        })
        self.assertEqual(settings.smtp_user, "legacy-user")
        self.assertEqual(settings.smtp_pass, "legacy-pass")
        self.assertEqual(settings.smtp_from, "legacy.sender@example.test")

    def test_new_variable_names_win_over_legacy_names(self):
        settings = load_settings({**BREVO_ENV, "SMTP_USERNAME": "legacy-user", "SMTP_PASSWORD": "legacy-pass"})
        self.assertEqual(settings.smtp_user, "brevo-smtp-login")
        self.assertEqual(settings.smtp_pass, "xsmtpsib-key")


if __name__ == "__main__":
    unittest.main()
