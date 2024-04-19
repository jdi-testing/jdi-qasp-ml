import base64
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.logger import logger
from app.models import ReportMail
from utils.config import (
    EMAIL_SENDER_LOGIN,
    EMAIL_SENDER_PASSWORD,
    RECIPIENT_EMAILS,
    SMTP_HOST,
)


def send_support_jdi(msg_content: ReportMail) -> None:

    subject = msg_content["subject"]
    header = f"{msg_content['subject']} from user {msg_content['email']}"
    body = f'<p>{msg_content["body"]}</p>'

    msg_to_send = MIMEMultipart()
    msg_to_send["Subject"] = Header(subject, "utf-8")
    msg_to_send["From"] = EMAIL_SENDER_LOGIN
    msg_to_send["To"] = RECIPIENT_EMAILS
    msg_to_send.attach(
        MIMEText(
            '<h2 style="margin: 0; padding: 10px; color: #ffffff; background: #4b9fc5">'
            + header
            + "</h2>"
            + body,
            "html",
            "utf-8",
        )
    )

    attachments_list = msg_content["attachments"]
    for file_dict in attachments_list:
        filename = file_dict["filename"]
        logger.info(f'File {filename} is attached to "Report Problem" email')
        file_content = file_dict["file_content"]

        file_content_in_bytes = base64.b64decode(file_content)
        part = MIMEApplication(_data=file_content_in_bytes, Name=filename)

        part["Content-Disposition"] = f"attachment; filename={filename}"
        part["Content-Transfer-Encoding"] = "base64"
        msg_to_send.attach(part)

    s = smtplib.SMTP(SMTP_HOST, 587, timeout=10)
    try:
        s.starttls()
        s.login(EMAIL_SENDER_LOGIN, EMAIL_SENDER_PASSWORD)
        s.sendmail(msg_to_send["From"], RECIPIENT_EMAILS, msg_to_send.as_string())
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        s.quit()


mail_backend_list = [send_support_jdi]
