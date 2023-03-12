import imaplib
import smtplib
import email
import email.header
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
logger = logging.getLogger('appToaster')

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
def sendEmail(to, title, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = "astlexbudler@naver.com"
    msg['To'] = to
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP_SSL('smtp.naver.com', 465)
    server.login("astlexbudler", "mic@6142xi4aem")
    server.send_message(msg)
    server.quit()

##################################################
# 작업 완료 이메일
##################################################
def jobsDone(icon, applicationName, url, designNote, expireDate, downloadLink, key):
    return ''' 
<table style="
width: 650px;
margin: auto;
padding: 25px 75px 25px 75px;
color: rgb(50, 50, 50);
font-size: 16px;
font-weight: 300;
word-break: break-all;">
    <thead>
        <tr>
            <td colspan="4">
                <img src="https://apptoaster.co.kr/static/apptoaster/images/logo/logo_black.png" style="
width: 250px;">
            </td>
        </tr>
        <tr>
            <td colspan="2" style="
padding: 15px 0px 15px 0px;">
                <hr style="
border: 0;
border-top: 1px solid gainsboro;">
            </td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="2" style="font-size: 12px; padding-bottom: 15px;">
                (''' + applicationName,  + ''')의 어플리케이션 변환 작업이 완료되었습니다!
            </td>
        </tr>
        <tr>
            <td colspan="2" style="padding-bottom: 15px;">
                작업 내용 요약
            </td>
        </tr>
        <tr>
            <td>
                어플리케이션 아이콘
            </td>
            <td>
                <img src="https://apptoaster.co.kr/''' + icon,  + '''" style="width: 100px;">
            </td>
        </tr>
        <tr>
            <td>
                어플리케이션 이름
            </td>
            <td>
                ''' + applicationName + '''
            </td>
        </tr>
        <tr>
            <td>
                웹 사이트 주소
            </td>
            <td>
                ''' + url + '''
            </td>
        </tr>
        <tr>
            <td>
                디자인
            </td>
            <td>
                ''' + designNote + '''
            </td>
        </tr>
        <tr>
            <td>
                만료일
            </td>
            <td>
                ''' + expireDate + '''
            </td>
        </tr>
        <tr>
            <td colspan="4" style="
padding: 15px 0px 15px 0px;">
                <hr style="
border: 0;
border-top: 1px solid gainsboro;">
            </td>
        </tr>
        <tr>
            <td colspan="2" style="font-size: 12px;">
                아래 링크를 통해 어플리케이션을 다운로드한 뒤 구글 플레이 및 애플 스토어 개발자 개정으로 어플리케이션을 등록하세요.
            </td>
        </tr>
        <tr>
            <td colspan="2" style="font-size: 12px;">
                링크: <a href="''' + downloadLink + '''">GoogleDriveLink</a>
            </td>
        </tr>
    </tbody>
</table>
<table style="
width: 650px;
margin: auto;
padding: 25px 75px 25px 75px;
color: rgb(50, 50, 50);
font-size: 16px;
font-weight: 300;
background-color: gainsboro;">
    <tr>
        <td colspan="2">
            <img src="https://apptoaster.co.kr/static/apptoaster/images/logo/logo_black.png" style="
width: 200px;">
        </td>
        <td colspan="2" style="font-size: 12px; padding-left: 50px;">
            <a href="https://apptoaster.co.kr/privacy" style="color: rgb(50, 50, 50);">개인정보 처리방침</a> 및 <a
                href="https://apptoaster.co.kr/policy" style="color: rgb(50, 50, 50);">이용약관</a><br>
            <a href="https://spam.kisa.or.kr/common/nttFileDownload.do?fileKey=2ed78e5844315de9e11ddd8219b283d0"
                style="color: rgb(50, 50, 50);">한국 인터넷 진흥원 푸시 메세지 사용 안내</a>
        </td>
    </tr>
    <tr>
        <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
            <a href="https://apptoaster.co.kr/toaster?key=''' + key + '''" style="color: rgb(50, 50, 50);">계정 확인</a>
            <span> / </span>
            <a href="https://apptoaster.co.kr/push_toasting?key=''' + key + '''" style="color: rgb(50, 50, 50);">푸시
                삭제/수정</a>
            <span> / </span>
            <a href="https://apptoaster.co.kr/push_toasted?key=''' + key + '''" style="color: rgb(50, 50, 50);">푸시 기록
                확인</a>
        </td>
    </tr>
    <tr>
        <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
            © 2023 <b>AppToaster</b>. All Rights Reserved.
        </td>
    </tr>
</table>
'''

##################################################
# 이메일 PUSH 도구
##################################################
def emailPushTool(applicationName, key):
    return '''
<form method="POST" action="https://apptoaster.co.kr/api/toast_push/key/''' + key  + '''" target="_blank">
    <table style="
    width: 650px;
    margin: auto;
    padding: 25px 75px 25px 75px;
    color: rgb(50, 50, 50);
    font-size: 16px;
    font-weight: 300;
    word-break: break-all;">
        <thead>
            <tr>
                <td>
                    <img src="https://apptoaster.co.kr/static/apptoaster/images/logo/logo_black.png" style="
    width: 250px;">
                </td>
                <td colspan="3" style="
    text-align: end;">
                    <span style="background-color: rgb(75, 75, 75); color: white;">
                        PUSH 보내기
                    </span>
                </td>
            </tr>
            <tr>
                <td colspan="4" style="
    padding: 15px 0px 15px 0px;">
                    <hr style="
    border: 0;
    border-top: 1px solid gainsboro;">
                </td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td colspan="4" style="font-size: 12px; padding-bottom: 15px;">
                    push to. ''' + applicationName + '''
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div style="display: inline-block;">
                        <label style="display: block;">이름(최대 24자)</label>
                        <input value="제목 없음" maxlength="24"
                            style="width: 215px; border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px;">
                    </div>
                    <div style="display: inline-block;">
                        <label style="display: block;">푸시 제목(최대 32자) <span style="color: red;">*</span></label>
                        <input value="''' + applicationName + '''" maxlength="32"
                            style="width: 274px; border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; margin-left: 4px;">
                    </div>
                </td>
            </tr>
            <tr>
                <td colspan="4" style="padding-top: 5px;">
                    <div style="display: inline-block;">
                        <label style="display: block;">푸시 내용(최대 255자) <span style="color: red;">*</span></label>
                        <textarea placeholder="메세지를 입력해주세요." maxlength="255"
                            style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 498px;"
                            required></textarea>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="padding-top: 5px;" colspan="4">
                    <div style="display: inline-block;">
                        <label style="display: block;">예약 선택 <span style="color: red;">*</span></label>
                        <select
                            style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 181px; margin-right: 4px;">
                            <option selected>
                                예약 안함
                            </option>
                            <option>
                                예약하고 한번
                            </option>
                            <option>
                                매일 반복
                            </option>
                        </select>
                    </div>
                    <div style="display: inline-block;">
                        <label style="display: block;">예약 날짜</label>
                        <input type="date"
                            style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 150px; margin-right: 4px;">
                    </div>
                    <div style="display: inline-block;">
                        <label style="display: block;">예약 시간</label>
                        <input type="time"
                            style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 150px;">
                    </div>
                </td>
            </tr>
            <tr>
                <td colspan="4" style="font-size: 12px; color: gray;">
                    * 예약 안함 선택 시 <span style="text-decoration: underline;">예약 날짜</span> 및 <span
                        style="text-decoration: underline;">예약 시간</span>을 입력하지 않으셔도 됩니다.<br>
                    * 매일 반복 선택 시 <span style="text-decoration: underline;">예약 날짜</span>을 입력하지 않으셔도 됩니다.
                </td>
            </tr>
            <tr>
                <td style="padding-top: 5px;" colspan="4">
                    <input type="checkbox">
                    <label>광고성 푸시 메세지 여부 <small>(광고성 푸시 메세지일 경우 체크박스 클릭)</small></label>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <input type="checkbox" required>
                    <label><a href="https://apptoaster.co.kr/privacy" style="color: rgb(50, 50, 50);">개인정보 처리 방침</a> 및
                        <a href="https://apptoaster.co.kr/policy" style="color: rgb(50, 50, 50);">이용약관</a> 동의 <span
                            style="color: red;">*</span></label>
                </td>
            </tr>
            <tr>
                <td colspan="4" style="padding-top: 50px;">
                    <button
                        style="border-radius: 0px; background-color: rgb(75, 75, 75); border: 0; color: white; padding: 10px 15px 10px 15px; width: 498px;">
                        보내기
                    </button>
                </td>
            </tr>
        </tbody>
    </table>
</form>
<table style="
width: 650px;
margin: auto;
padding: 25px 75px 25px 75px;
color: rgb(50, 50, 50);
font-size: 16px;
font-weight: 300;
background-color: gainsboro;">
    <tr>
        <td colspan="2">
            <img src="https://apptoaster.co.kr/static/apptoaster/images/logo/logo_black.png" style="
width: 200px;">
        </td>
        <td colspan="2" style="font-size: 12px; padding-left: 50px;">
            <a href="https://apptoaster.co.kr/privacy" style="color: rgb(50, 50, 50);">개인정보 처리방침</a> 및 <a
                href="https://apptoaster.co.kr/policy" style="color: rgb(50, 50, 50);">이용약관</a><br>
            <a href="https://spam.kisa.or.kr/common/nttFileDownload.do?fileKey=2ed78e5844315de9e11ddd8219b283d0"
                style="color: rgb(50, 50, 50);">한국 인터넷 진흥원 푸시 메세지 사용 안내</a>
        </td>
    </tr>
    <tr>
        <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
            <a href="https://apptoaster.co.kr/toaster?key=''' + key + '''" style="color: rgb(50, 50, 50);">계정 확인</a>
            <span> / </span>
            <a href="https://apptoaster.co.kr/push_toasting?key=''' + key  + '''" style="color: rgb(50, 50, 50);">푸시
                삭제/수정</a>
            <span> / </span>
            <a href="https://apptoaster.co.kr/push_toasted?key=''' + key  + '''" style="color: rgb(50, 50, 50);">푸시 기록
                확인</a>
        </td>
    </tr>
    <tr>
        <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
            © 2023 <b>AppToaster</b>. All Rights Reserved.
        </td>
    </tr>
</table>
'''
