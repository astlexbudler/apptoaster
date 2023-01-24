import json
import imaplib
import email
import email.header
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import hmac
import hashlib
import requests
import random
import datetime
from .models import *

import logging
logger = logging.getLogger('appToaster')


##################################################
# 이메일
##################################################
##################################################
# 읽지 않은 이메일 조회
##################################################
def checkNewEmail():

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
            "title": headDecoder(email_message["Title"]),
            "content": bodyDecoder(raw_email_string),
        })

        # 해당 메일을 읽음으로 표시
        imap.store(mail, '+FLAGS', '\\Seen')

    # imap 종료
    imap.close()

    return email_list

##################################################
# 이메일 송신
##################################################
def sendEmail(to, title, content):
    # 기본정보
    email_address = "stackable01@naver.com"
    password = "mic6142xi4aem"
    smtp_server = 'smtp.naver.com'
    port = 587

    # 데이터 정리
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = email_address
    msg['To'] = to
    msg.attach(MIMEText(content, 'html'))

    # smtp 발송
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.login(email_address, password)
    server.send_message(msg)
    server.quit()


##################################################
# 카카오 PUSH API
##################################################
##################################################
# 푸시 토큰 등록하기
##################################################
def kakaoRegisterPushToken(kakao_app_admin_key, uuid, device_id, push_type, push_token):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/register'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'KakaoAK ' + kakao_app_admin_key,
    }
    body = {
        'uuid':uuid,
        'device_id':device_id,
        'push_type':push_type,
        'push_token':push_token
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

##################################################
# 푸시 토큰 보기
##################################################
def kakaoGetPushToken(kakao_app_admin_key, uuid):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/tokens?uuid=' + uuid

    # header 및 body 작성
    header = {
        'Authorization': 'KakaoAK ' + kakao_app_admin_key,
    }

    # API 요청
    response = requests.get(url, headers=header)

    return response

##################################################
# 푸시 토큰 삭제하기
##################################################
def kakaoDeletePushToken(kakao_app_admin_key, uuid, device_id, push_type):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/deregister'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + kakao_app_admin_key,
    }
    body = {
        'uuid':uuid,
        'device_id':device_id,
        'push_type':push_type
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

    return response

##################################################
# 푸시 알림 보내기
##################################################
def kakaoSendPushNotification(kakao_app_admin_key, title, message, uuid_list):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/send'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + kakao_app_admin_key,
    }
    push_message = {
        "for_fcm":{
            "notification":{
                "title":title,
                "body":message,
            }
        }
    }
    body = {
        'uuids':'["1234"]',
        'push_message':json.dumps(push_message),
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

    return response