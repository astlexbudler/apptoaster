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
    # me == my email address
    # you == recipient's email address
    me = "astlexbudler@naver.com"
    you = to

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
        How are you?<br>
        Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.naver.com', 465)

    mail.ehlo()

    mail.starttls()

    mail.login('astlexbudler', 'Mic6142hi@sdq')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()