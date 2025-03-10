import smtplib
from email.mime.text import MIMEText
from config import Config

def send_confirmation_email(to_email: str):
    msg = MIMEText("مرحبًا! الرجاء تأكيد حسابك.")
    msg['Subject'] = 'تأكيد حساب البوت'
    msg['From'] = Config.EMAIL_USER
    msg['To'] = to_email

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
        server.send_message(msg)