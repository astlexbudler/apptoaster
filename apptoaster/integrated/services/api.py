import requests
import json
import logging
logger = logging.getLogger('appToaster')

'''
api.py
API 관련 기능을 관리하는 서비스입니다.
'''

##################################################
# 카카오 PUSH API
##################################################
##################################################
# 푸시 토큰 등록하기
##################################################
def kakaoRegisterTarget(kakaoAppAdminKey, uuid, token):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/register'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + kakaoAppAdminKey,
    }
    body = {
        'uuid':uuid,
        'device_id':uuid,
        'push_type':'fcm',
        'push_token':token
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

    return response

##################################################
# 푸시 토큰 보기
##################################################
def kakaoGetTarget(kakaoAppAdminKey, uuid):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/tokens?uuid=' + uuid

    # header 및 body 작성
    header = {
        'Authorization': 'KakaoAK ' + kakaoAppAdminKey,
    }

    # API 요청
    response = requests.get(url, headers=header)

    return response

##################################################
# 푸시 토큰 삭제하기
##################################################
def kakaoDeleteTarget(kakaoAppAdminKey, uuid):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/deregister'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + kakaoAppAdminKey,
    }
    body = {
        'uuid':uuid,
        'device_id':uuid,
        'push_type':'fcm'
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

    return response

##################################################
# 푸시 알림 보내기
##################################################
def kakaoSendPush(kakaoAppAdminKey, title, message, targetList):
    # 기본정보
    url = 'https://kapi.kakao.com/v2/push/send'

    # header 및 body 작성
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Authorization': 'KakaoAK ' + kakaoAppAdminKey,
    }
    push_message = {
        "for_fcm":{
            "notification":{
                "title":title,
                "body":message
            }
        }
    }

    uuids = '['
    for target in targetList:
        uuids += '"' + target['uuid'] + '",'
    uuids = uuids[0:-1] + ']'

    body = {
        'uuids':uuids,
        'push_message':json.dumps(push_message)
    }

    # API 요청
    response = requests.post(url, headers=header, data=body)

    return response