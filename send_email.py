from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json

with open('./email_info.json') as f:
    SETTING = json.load(f)


print(SETTING)