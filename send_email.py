from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json

with open('./email_info.json') as f:
    SETTING = json.load(f)


print(SETTING.SERVER)

smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587) # SMTP 서버 TSL방식으로 접속

hello_message = smtp_server.ehlo() # SMTP서버에 hello 메시지 보냄
print(hello_message,"\n")

bye_message = smtp_server.quit() # 종료
print(bye_message)