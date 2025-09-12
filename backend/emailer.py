# backend/emailer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Example using Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "am18th@gmail.com"       # replace with your Gmail
FROM_PASSWORD = "mbfutozweydbijlc"      # generate App Password from Google

def send_email(to_email: str, subject: str, html_content: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "sent"
    except Exception as e:
        print("Email error:", e)
        return "error"
