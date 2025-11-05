import smtplib
from email.message import EmailMessage
from flask import current_app

def send_email(subject, recipient, html_body, text_body=None):
    """
    Minimal email sender: uses SMTP server configured by MAIL_SERVER & MAIL_PORT.
    In dev you can run `python -m smtpd -n -c DebuggingServer localhost:8025`
    which will print emails to console.
    """
    cfg = current_app.config
    sender = cfg.get("MAIL_DEFAULT_SENDER")
    server = cfg.get("MAIL_SERVER")
    port = cfg.get("MAIL_PORT")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    if text_body:
        msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(server, port) as smtp:
            smtp.send_message(msg)
        current_app.logger.info(f"Email sent to {recipient}")
        return True
    except Exception as e:
        current_app.logger.warning(f"Failed to send email: {e}")
        # fallback: print to console
        print("=== Email fallback ===")
        print(msg)
        return False
