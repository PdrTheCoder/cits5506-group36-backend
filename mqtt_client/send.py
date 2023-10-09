# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

MAIL_HOST = 'smtp-mail.outlook.com'
MAIL_PORT = 587
MAIL_USER = 'cits55062023@outlook.com'
MAIL_PASS = 'group36Qaz'

def sendmail(receiver, content, subject):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = MAIL_USER
    msg['To'] = receiver

    s = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    s.starttls()
    s.login(MAIL_USER, MAIL_PASS)
    s.send_message(msg)
    s.quit()
