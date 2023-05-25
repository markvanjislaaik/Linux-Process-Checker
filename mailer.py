import json
import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logger = logging.getLogger(__name__)


class EmailSender:

    def __init__(self, config_file: str='credentials.json') -> None:

        with open(config_file, 'r') as f:
            data = json.load(f)

        self.host_access_key = data.get('host_access_key')
        self.smtp_server = data.get('smtp_server')
        self.port = data.get('port')
        self.password = data.get('host_secret_key')
        self.sender_email = data.get('sender_email')
        self.sender_name = data.get('sender_name')
        self.default_recipients = data.get('default_recipients')

    def send_email(self, subject: str, custom_content: str, header: str,
                   recipients: any=None, attachments: list[str]=None) -> None:

        if not recipients:
            recipients = ', '.join(self.default_recipients)
        elif isinstance(recipients, str):
            recipients = ', '.join([recipients])
        elif isinstance(recipients, list):
            recipients = ', '.join(recipients)

        message = MIMEMultipart('alternative')
        message['From'] = f"{self.sender_name} <{self.sender_email}>"
        message['To'] = recipients
        message['Subject'] = subject

        content = f"""
            <h2>{header}</h2>
            {custom_content}
            <br>
            <p>Support Services</p>
            <br>
            <small>Contact support@example.com with any queries.</small>
            <br>
        """

        message.attach(MIMEText(content, 'html'))

        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                with open(attachment, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {attachment}')
                message.attach(part)

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()
            server.starttls()
            server.login(self.host_access_key, self.password)
            server.send_message(message)