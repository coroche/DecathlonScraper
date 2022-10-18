import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import os
from dotenv import load_dotenv

load_dotenv()

port = os.getenv('port')
smtp_server = os.getenv('smtp_server')
sender_email = os.getenv('sender_email') 
password = os.getenv('password')
errorEmail = os.getenv('error_email')

def sendEmail(html, receiver_email, subject):
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def sendErrorEmail():
    html = """\
<html>
  <body>
    <p>Error checking decathlon stock</p>
  </body>
</html>
"""
    message = MIMEMultipart()
    message["Subject"] = 'DecaBot Error'
    message["From"] = sender_email
    message["To"] = errorEmail
    message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, errorEmail, message.as_string())