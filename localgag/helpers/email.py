import smtplib

from localgag import settings


class EmailClient:

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

    def send_email(self, to, message):
        self.server.sendmail(settings.SMTP_USERNAME, to, message)
