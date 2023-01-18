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
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import random
import datetime

logger = logging.getLogger(__name__)

##################################################
# 사용자 IP 확인
##################################################
def getIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

##################################################
# 타임스탬프 생성
##################################################
def timestamp():
    return  datetime.datetime.now().strftime("%Y%m%d%H%M%S")

##################################################
# 랜덤 숫자/문자 생성
##################################################
def getRandomString(length):
    str = ''
    pool = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKKLZXCVBNM'

    for i in range(length):
        str += random.choice(pool)
    
    return str

def getRandomNumber(length):
    str = ''
    pool = '1234567890'
        
    for i in range(length):
        str += random.choice(pool)
    
    return str

##################################################
# 스케줄러
##################################################
def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', seconds=10)
    scheduler.start()

def scheduled_job():
    #print(str(int(time.time()*1000)))
    return

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
            "Title": headDecoder(email_message["Title"]),
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

'''
    service_id = "ncp:push:kr:286110826848:apptoaster"
    access_key = "3INXdVk5GlpxRa1vX6Ay"
    secret_key = "97RY3iEdnVQJXbjGF7QI016whXOEN9TyJr5dA72s"
'''
##################################################
# 네이버 PUSH API
##################################################
##################################################
# 새로운 디바이스 등록
##################################################
def registerNotificationDevice(service_id, access_key, secret_key, user_id, device_type, fcm_token, is_ad, is_night):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/users"
    sign_url = "/push/v2/services/" + service_id + "/users"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')

    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }
    body = {
        "userId":user_id,
        "country":"KR",
        "language":"ko",
        "timezone":32400,
        "channelName":"main",
        "deviceType":device_type,
        "deviceToken":fcm_token,
        "isNotificationAgreement":True,
        "isAdAgreement":is_ad,
        "isNightAdAgreement":is_night
    }

    # API 요청
    return requests.post(url, headers=header, data=json.dumps(body))

##################################################
# 등록된 디바이스 검색
##################################################
def findNotificationDevice(service_id, access_key, secret_key, user_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/users/" + user_id
    sign_url = "/push/v2/services/" + service_id + "/users/" + user_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.get(url, headers=header)

##################################################
# 등록된 디바이스 삭제
##################################################
def deleteNotificationDevice(service_id, access_key, secret_key, user_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/users/" + user_id
    sign_url = "/push/v2/services/" + service_id + "/users/" + user_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "DELETE"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.delete(url, headers=header)

##################################################
# 새로운 알림 채널 생성
##################################################
def createNotificationChannel(service_id, access_key, secret_key, channel_name, channel_desc):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels"
    sign_url = "/push/v2/services/" + service_id + "/channels"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }
    body = {
        "channelName":channel_name,
        "channelDesc":channel_desc,
    }

    # API 요청
    return requests.post(url, headers=header, data=json.dumps(body))

##################################################
# 알림 채널들 업데이트
##################################################
def putNotificationChannels(service_id, access_key, secret_key, channel_list):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels"
    sign_url = "/push/v2/services/" + service_id + "/channels"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "PUT"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }
    body = []
    for channel in channel_list:
        body.append({
        "channelName":channel["channel_name"],
        "channelDesc":channel["channel_desc"],
    })

    # API 요청
    return requests.put(url, headers=header, data=json.dumps(body))

##################################################
# 등록된 알림들 채널 검색
##################################################
def getNotificationChannels(service_id, access_key, secret_key):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels"
    sign_url = "/push/v2/services/" + service_id + "/channels"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.get(url, headers=header)

##################################################
# 등록된 알림 채널들 삭제
##################################################
def deleteNotificationChannels(service_id, access_key, secret_key, channel_list):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels"
    sign_url = "/push/v2/services/" + service_id + "/channels"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "DELETE"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }
    body = []
    for channel in channel_list:
        body.append({
        "channelName":channel["channel_name"],
    })

    # API 요청
    return requests.delete(url, headers=header, data=json.dumps(body))

##################################################
# 채널에 디바이스 등록
##################################################
def registerChannelUser(service_id, access_key, secret_key, channel_name, user_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels/" + channel_name + "/users/" + user_id
    sign_url = "/push/v2/services/" + service_id + "/channels/" + channel_name + "/users/" + user_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.post(url, headers=header)

##################################################
# 채널에서 디바이스 삭제
##################################################
def deleteChannelUser(service_id, access_key, secret_key, channel_name, user_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/channels/" + channel_name + "/users/" + user_id
    sign_url = "/push/v2/services/" + service_id + "/channels/" + channel_name + "/users/" + user_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "DELETE"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.delete(url, headers=header)

##################################################
# 알림 생성
##################################################
def sendNotification(service_id, access_key, secret_key, notification_type, notification_message, is_reserve, reserve_time, is_schedule, schedule_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/messages"
    sign_url = "/push/v2/services/" + service_id + "/messages"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }
    body = {
        "messageType": notification_type,
        "target": {
            "type": "ALL",
            "country": ["KR"]
        },
        "message": {
            "default": {
                "content": "",
                "custom": {
                    "title": "this_is_title",
                    "content": "this_is_content",
                }
            },
        },
    }
    if is_reserve:
        body.update({
            "reserveTime": reserve_time,
        })
    if is_schedule:
        body.update({
            "scheduleCode": schedule_id,
        })

    # API 요청
    return requests.post(url, headers=header, data=json.dumps(body))

##################################################
# 알림 검색
##################################################
def notificationCheck(service_id, access_key, secret_key, request_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/messages/" + request_id
    sign_url = "/push/v2/services/" + service_id + "/messages/" + request_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.get(url, headers=header)

##################################################
# 예약 알림 검색
##################################################
def reserveCheck(service_id, access_key, secret_key, request_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/reservations/" + request_id + "/reserve-status"
    sign_url = "/push/v2/services/" + service_id + "/reservations/" + request_id + "/reserve-status"
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.get(url, headers=header)

##################################################
# 예약 알림 삭제
##################################################
def reserveCancel(service_id, access_key, secret_key, request_id):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/reservations/" + request_id
    sign_url = "/push/v2/services/" + service_id + "/reservations/" + request_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "DELETE"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.delete(url, headers=header)

##################################################
# 정기 알림 삭제
##################################################
def scheduleCancel(service_id, access_key, secret_key, request_id, schedule_code):
    # 기본정보
    url = "https://sens.apigw.ntruss.com/push/v2/services/" + service_id + "/schedules/" + schedule_code + "/messages/" + request_id
    sign_url = "/push/v2/services/" + service_id + "/schedules/" + schedule_code + "/messages/" + request_id
    timestamp = str(int(time.time()*1000))
    secret_key = bytes(secret_key, 'UTF-8')
    method = "DELETE"
    message = bytes((method + " " + sign_url + "\n" + timestamp + "\n" + access_key), 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
    
    # header 및 body 작성
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingKey,
    }

    # API 요청
    return requests.delete(url, headers=header)

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
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
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