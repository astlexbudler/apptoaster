import requests
import json
import logging
import http.client
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

##################################################
# 토스 결제/빌링 API
##################################################
#결제승인요청
def tosspayments_approval(dict):  # 결제 승인 API 요청
    conn = http.client.HTTPSConnection("api.tosspayments.com")
    paymentKey = dict["paymentKey"]
    amount = dict["amount"]
    orderId = dict["orderId"]
    innerpayload = f"@paymentKey@:@{paymentKey}@,@amount@:{amount},@orderId@:@{orderId}@"
    payload = "{" + innerpayload + "}"
    payload = payload.replace("@","\"")

    headers = {
        'Authorization': "Basic dGVzdF9za19ZWjFhT3dYN0s4bXhkQXZPZDk5cnlReHp2TlBHOg==",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/v1/payments/confirm", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

#빌링연동요청
def tossbilling_approval(dict):
    authKey = dict["authKey"]
    customerKey = dict["customerKey"]
    import http.client

    conn = http.client.HTTPSConnection("api.tosspayments.com")

    innerpayload = f"@authKey@:@{authKey}@,@customerKey@:@{customerKey}@"
    payload = "{" + innerpayload + "}"
    payload = payload.replace("@","\"")

    headers = {
        'Authorization': "Basic dGVzdF9za19ZWjFhT3dYN0s4bXhkQXZPZDk5cnlReHp2TlBHOg==",
        'Content-Type': "application/json; charset=utf-8",
        }

    conn.request("POST", "/v1/billing/authorizations/issue", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

#빌링결제요청
def tossbilling_payment_approval(dict):
    conn = http.client.HTTPSConnection("api.tosspayments.com")
    customerKey = dict["customerKey"]
    billingKey = dict["billingKey"]
    amount = dict["amount"]
    orderId = dict["orderId"]
    orderName = dict["orderName"]
    innerpayload = f"@customerKey@:@{customerKey}@,@amount@:{amount},@orderId@:@{orderId}@,@orderName@:@{orderName}@"
    payload = "{" + innerpayload + "}"
    payload = payload.replace("@","\"")
    payload = payload.encode('utf-8')
    headers = {
        'Authorization': "Basic dGVzdF9za19ZWjFhT3dYN0s4bXhkQXZPZDk5cnlReHp2TlBHOg==",
        'Content-Type': "application/json; charset=utf-8"
    }
    conn.request("POST", f"/v1/billing/{billingKey}", payload, headers)

    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))