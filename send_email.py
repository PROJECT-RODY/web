from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import smtplib
import json
import re


class email_sender():
    def __init__(self,):
        with open('./email_info.json') as f:
            SETTING = json.load(f)

        self.server_add = SETTING['SERVER']
        self.server_port = SETTING['PORT']
        self.sender = SETTING['USER']
        self.sender_pw = SETTING['PASSWORD']

    def email_check(self, email):
        regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if re.match(regex, email):
            return True
        return False

    def send_pdf(self, emails, subject, content, attach=None):
        for email in emails:
            if not self.email_check(email):
                print("이메일 주소 오류")
                return False
            
            if attach:
                mime=MIMEMultipart('mixed')
            else :
                mime=MIMEMultipart('alternative')

            mime['From'] = self.sender
            mime['To'] = email
            mime['Subject'] = subject

            contents = content
            text = MIMEText(_text = contents, _charset = 'utf-8')
            mime.attach(text)

            if attach:
                data = MIMEBase('application', 'octect-stream')
                data.set_payload(open(attach, 'rb').read())
                encoders.encode_base64(data)

                filename = os.path.basename(attach)
                data.add_header('Content-Disposition', 'attachment', filename=('UTF-8', '', filename))
                mime.attach(data)

            smtp = smtplib.SMTP_SSL(self.server_add, self.server_port)
            smtp.login(self.sender, self.sender_pw)
            smtp.sendmail(self.sender, email, mime.as_string())
            smtp.close()
            print("메일 발송 완료")
            return True

def send_pdf(self, email, subject, content, attach=None): # 함수화 시킨것 사용.
    regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if not re.match(regex, email):
        return False
        
    print(email, subject)
    if attach:
        mime=MIMEMultipart('mixed')
    else :
        mime=MIMEMultipart('alternative')

    mime['From'] = self.sender
    mime['To'] = email
    mime['Subject'] = subject

    contents = content
    text = MIMEText(_text = contents, _charset = 'utf-8')
    mime.attach(text)

    if attach:
        data = MIMEBase('application', 'octect-stream')
        data.set_payload(open(attach, 'rb').read())
        encoders.encode_base64(data)

        filename = os.path.basename(attach)
        data.add_header('Content-Disposition', 'attachment', filename=('UTF-8', '', filename))
        mime.attach(data)

    smtp = smtplib.SMTP_SSL(self.server_add, self.server_port)
    smtp.login(self.sender, self.sender_pw)
    smtp.sendmail(self.sender, email, mime.as_string())
    smtp.close()
    
    return True

if __name__ == '__main__':
    emails = ["minchan1472@naver.com", "minchan1472@gmail.com",'skdk@jd@.dkd@,d,']
    email_sender = email_sender()
    # email_sender.send_pdf(emails, '제목', '내용', './user_image/single_s9.png')
    email_sender.send_pdf(emails, '제목', '내용', './pdf/single_s9.pdf')