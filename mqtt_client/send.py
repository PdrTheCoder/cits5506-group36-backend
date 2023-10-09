# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

MAIL_HOST = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USER = 'paynemax@163.com'
MAIL_PASS = 'JEFQZOCDXIJSNIES'

def sendmail(receiver, content, subject):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = MAIL_USER
    msg['To'] = receiver

    s = smtplib.SMTP()
    s.connect(MAIL_HOST, MAIL_PORT)
    s.login(MAIL_USER, MAIL_PASS)
    s.send_message(msg)
    s.quit()
