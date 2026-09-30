from __future__ import annotations

import logging
import smtplib
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formataddr

from app.config import get_settings

logger = logging.getLogger("grievance.email")

EMAIL_STATUS_EVENTS = frozenset({"in_progress", "resolved"})
SMTP_TIMEOUT_SECONDS = 10


def smtp_configuration_ready(settings) -> bool:
    """Report whether the configured SMTP settings can actually deliver a message."""
    if not settings.smtp_host or not settings.smtp_from:
        return False
    # A relay that needs no credentials is allowed, but a half-filled login is not.
    return bool(settings.smtp_user) == bool(settings.smtp_pass)


def smtp_server_label(settings) -> str:
    """Return a credential-free SMTP description for startup and debug logging."""
    if not smtp_configuration_ready(settings):
        return "not configured"
    return f"{settings.smtp_host}:{settings.smtp_port}"


def email_event_for_status_transition(old_status: str | None, new_status: str) -> str | None:
    """Return an email event only for a real transition into an allowed state."""
    old = (old_status or "").strip().lower().replace(" ", "_")
    new = (new_status or "").strip().lower().replace(" ", "_")
    if new in EMAIL_STATUS_EVENTS and old != new:
        return new
    return None


def _format_datetime(value: datetime | None) -> str:
    timestamp = value or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone().strftime("%d %b %Y, %I:%M %p %Z")


def _build_message(
    event: str,
    *,
    recipient_email: str,
    citizen_name: str,
    grievance_id: str,
    complaint_text: str,
    occurred_at: datetime | None,
    previous_status: str | None,
) -> EmailMessage | None:
    if event == "submitted":
        subject = f"Grievance {grievance_id} Submitted Successfully"
        body = (
            f"Hello {citizen_name},\n\n"
            "Your grievance has been successfully submitted.\n\n"
            f"Grievance ID: {grievance_id}\n"
            f"Complaint: {complaint_text}\n"
            "Status: SUBMITTED\n"
            f"Submission date/time: {_format_datetime(occurred_at)}\n\n"
            "Your complaint has been successfully registered in the grievance management system.\n"
            "You can log in to the portal to track its progress.\n\n"
            "Regards,\nAI Grievance Management System"
        )
    elif event == "in_progress":
        subject = f"Grievance {grievance_id} Is Now In Progress"
        previous = (previous_status or "UNKNOWN").replace("_", " ").upper()
        body = (
            f"Hello {citizen_name},\n\n"
            "There is an update regarding your grievance.\n\n"
            f"Grievance ID: {grievance_id}\n"
            f"Complaint: {complaint_text}\n"
            f"Previous status: {previous}\n"
            "Current status: IN_PROGRESS\n"
            f"Date/time: {_format_datetime(occurred_at)}\n\n"
            "Your complaint is currently being processed by the concerned department.\n\n"
            "Regards,\nAI Grievance Management System"
        )
    elif event == "resolved":
        subject = f"Grievance {grievance_id} Has Been Resolved"
        body = (
            f"Hello {citizen_name},\n\n"
            "Your grievance has been resolved.\n\n"
            f"Grievance ID: {grievance_id}\n"
            f"Complaint: {complaint_text}\n"
            "Status: RESOLVED\n"
            f"Resolution date/time: {_format_datetime(occurred_at)}\n\n"
            "The concerned department has marked your complaint as resolved.\n"
            "Please log in to the grievance portal to view the latest details.\n\n"
            "Regards,\nAI Grievance Management System"
        )
    else:
        return None

    message = EmailMessage()
    settings = get_settings()
    message["Subject"] = subject
    message["From"] = formataddr((settings.smtp_from_name, settings.smtp_from))
    message["To"] = recipient_email
    message.set_content(body)
    return message


@contextmanager
def smtp_session(settings) -> Iterator[smtplib.SMTP]:
    """Yield an SMTP session to the relay with transport encryption already enabled.

    `SMTP_SECURE` (Brevo port 465) uses implicit TLS. Otherwise the session is upgraded
    with STARTTLS, and a server that does not offer STARTTLS is refused so the login
    credentials are never sent in clear text.
    """
    if settings.smtp_secure:
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=SMTP_TIMEOUT_SECONDS) as smtp:
            yield smtp
        return
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=SMTP_TIMEOUT_SECONDS) as smtp:
        smtp.ehlo()
        if not smtp.has_extn("starttls"):
            raise smtplib.SMTPNotSupportedError("SMTP server does not support STARTTLS")
        smtp.starttls()
        smtp.ehlo()
        yield smtp


def send_complaint_notification(
    event: str,
    recipient_email: str | None,
    citizen_name: str | None,
    grievance_id: str,
    complaint_text: str,
    occurred_at: datetime | None = None,
    previous_status: str | None = None,
) -> None:
    """Send one plain-text SMTP notification; failures never escape to the API."""
    event = (event or "").strip().lower().replace(" ", "_")
    if event not in {"submitted", *EMAIL_STATUS_EVENTS}:
        logger.warning("Email notification skipped for unsupported event %s", event or "<empty>")
        return
    if not recipient_email:
        logger.warning("Email notification skipped for %s: citizen has no email address", event)
        return

    settings = get_settings()
    if not smtp_configuration_ready(settings):
        logger.warning("Email notification for %s skipped: SMTP configuration is incomplete", event)
        return

    message = _build_message(
        event,
        recipient_email=recipient_email,
        citizen_name=citizen_name or "Citizen",
        grievance_id=grievance_id,
        complaint_text=complaint_text,
        occurred_at=occurred_at,
        previous_status=previous_status,
    )
    try:
        with smtp_session(settings) as smtp:
            if settings.smtp_user:
                smtp.login(settings.smtp_user, settings.smtp_pass)
            smtp.send_message(message)
        logger.info("Email notification sent: event=%s grievance_id=%s", event, grievance_id)
    except Exception as exc:
        # Do not log exception text or SMTP configuration; authentication/network
        # errors must not leak credentials into application logs.
        logger.error(
            "Email notification failed: event=%s grievance_id=%s error_type=%s",
            event,
            grievance_id,
            type(exc).__name__,
        )
