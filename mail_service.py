import logging
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

SMTP_HOST = "localhost"
SMPTP_PORT = 1025
SENDER_EMAIL = "admin@gmail.com"
SENDER_PASSWORD = ''

def send_email(to, subject , content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))

    client = SMTP(host=SMTP_HOST, port=SMPTP_PORT)
    client.send_message(msg=msg)
    logging.debug("Email sent successfully.")
    client.quit()