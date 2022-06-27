import base64
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.logger import logger
from utils.config import (EMAIL_SENDER_LOGIN, EMAIL_SENDER_PASSWORD,
                          RECIPIENT_EMAILS, SMTP_HOST)


def send_support_jdi(msg_content):

    email_sender_login = EMAIL_SENDER_LOGIN
    email_sender_password = EMAIL_SENDER_PASSWORD
    smtp_host = SMTP_HOST
    recipients_emails = RECIPIENT_EMAILS

    subject = msg_content["subject"]
    header = f"{msg_content['subject']} from user {msg_content['email']}"
    body = f'<p>{msg_content["body"]}</p>'
    json_from_model = f"{msg_content['json_from_model']}"

    msg_to_send = MIMEMultipart()
    msg_to_send["Subject"] = Header(subject, "utf-8")
    msg_to_send["From"] = email_sender_login
    msg_to_send["To"] = recipients_emails
    msg_to_send.attach(
        MIMEText(
            '<h2 style="margin: 0; padding: 10px; color: #ffffff; background: #4b9fc5">'
            + header
            + "</h2>"
            + body
            + f"Response from model: {json_from_model}",
            "html",
            "utf-8",
        )
    )
    screenshot_in_bytes = base64.b64decode(msg_content["screenshot"])
    part = MIMEApplication(_data=screenshot_in_bytes, Name="screenshot.jpg")

    part["Content-Disposition"] = 'attachment; filename="screenshot.jpg"'
    part["Content-Transfer-Encoding"] = "base64"
    msg_to_send.attach(part)

    s = smtplib.SMTP(smtp_host, 587, timeout=10)
    try:
        s.starttls()
        s.login(email_sender_login, email_sender_password)
        s.sendmail(msg_to_send["From"], recipients_emails, msg_to_send.as_string())
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        s.quit()


mail_backend_list = [send_support_jdi]
