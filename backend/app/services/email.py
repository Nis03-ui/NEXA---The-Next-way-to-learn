import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
) -> None:
    """
    Send an HTML email through the configured SMTP server.
    """

    if not settings.smtp_username:
        raise RuntimeError(
            "SMTP_USERNAME is not configured"
        )

    if not settings.smtp_password:
        raise RuntimeError(
            "SMTP_PASSWORD is not configured"
        )

    from_email = (
        settings.smtp_from_email
        or settings.smtp_username
    )

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = (
        f"{settings.smtp_from_name} "
        f"<{from_email}>"
    )
    message["To"] = to_email

    message.set_content(
        "Please open this email in an HTML-compatible "
        "email client."
    )

    message.add_alternative(
        html_content,
        subtype="html",
    )

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port,
        timeout=20,
    ) as server:

        server.ehlo()

        server.starttls()

        server.ehlo()

        server.login(
            settings.smtp_username,
            settings.smtp_password,
        )

        server.send_message(message)