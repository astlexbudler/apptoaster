import imaplib
import smtplib
import email
import email.header
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''
email.py
이메일 관련 기능을 관리하는 서비스입니다.
'''

##################################################
# 이메일 수신함 확인
##################################################
def getEmail():
    # 메일 헤더 디코더
    def headDecoder(str):
        str = str.replace("=?utf-8?B?", "")
        str = str[0:str.find("?=")]
        return base64.b64decode(str).decode('utf-8')

    # 메일 바디 디코더
    def bodyDecoder(str):
        start = str.find('text/plain') + 68
        str = str[start:len(str)]
        end = str.find("\r\n\r\n")
        str = str[0:end]
        return base64.b64decode(str).decode('utf-8')[0:-1]
        
    # 기본 정보
    imap_server = "imap.naver.com"
    port = 993
    id = "stackable01"
    password = "mic6142xi4aem"

    # imap 생성 및 로그인
    imap = imaplib.IMAP4_SSL(imap_server, port)
    imap.login(id, password)

    # 받은 편지함 내 읽지 않은 메일 확인
    imap.select("INBOX")
    data = imap.search(None, "New")
    
    # 메일 확인
    email_list = []
    all_email = data[0].split()
    for mail in all_email:
        data = imap.fetch(mail, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # 메일 정보 파싱
        email_list.append({
            "from": headDecoder(email_message["From"]),
            "Title": headDecoder(email_message["Title"]),
            "content": bodyDecoder(raw_email_string),
        })

        # 해당 메일을 읽음으로 표시
        imap.store(mail, '+FLAGS', '\\Seen')

    # imap 종료
    imap.close()

    return email_list



##################################################
# 이메일 발송하기
##################################################
def sendEmail(to, title, content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = "astlexbudler@naver.com"
    msg['To'] = to
    msg.attach(MIMEText(content, 'html'))

    server = smtplib.SMTP('smtp.naver.com', 995)
    server.ehlo()
    server.starttls()
    server.login("astlexbudler@naver.com", "Mic6142hi@sdq")
    server.send_message(msg)
    server.quit()