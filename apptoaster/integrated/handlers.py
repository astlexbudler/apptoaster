import json
import imaplib
import email
from . import models
from . import utilities
import logging

logger = logging.getLogger(__name__)

##################################################
# 앱 토스터 API
##################################################
##################################################
# 사용자 등록(POST)
##################################################
def apptoasterSetUserHandler(request):
    # Logger
    ip = utilities.getIp(request)
    key = 'UNKNOWN'
    log = utilities.timestamp() + ' - '

    # request method 확인
    if request.method != 'POST':
        log += key + '(' + ip + ') - apptoasterSetUser() - error - request method error;'
        logger.warning(log)
        return json.dumps({
            'result':'request method error'
        })

    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
        key = request_dictionary['key']
        user_id = request_dictionary['user_id']
        device_token = request_dictionary['device_token']
    except:
        log += key + '(' + ip + ') - apptoasterSetUser() - error - json decode error;'
        logger.warning(log)
        return json.dumps({
            'result':'json decode error'
        })

    log += key + '(' + ip + ') - apptoasterSetUser() - user_id(' + user_id + ') has settled to device_token(' + device_token + ');'
    logger.info(log)
    
    return

##################################################
# 사용자 확인(GET)
##################################################
def apptoasterGetUserHandler(request):
    # Logger
    ip = utilities.getIp(request)
    key = 'UNKNOWN'
    log = utilities.timestamp() + ' - '

    # request method 확인
    if request.method != 'GET':
        log += key + '(' + ip + ') - apptoasterGetUser() - error - request method error;'
        logger.warning(log)
        return json.dumps({
            'result':'request method error'
        })

    # GET 데이터 수신
    try:
        key = request.GET['key']
        user_id = request.GET['user_id']
    except:
        log += key + '(' + ip + ') - apptoasterGetUser() - error - required parameter error;'
        logger.warning(log)
        return json.dumps({
            'result':'required parameter error'
        })

    log += key + '(' + ip + ') - apptoasterGetUser() - get user(' + user_id + ') info;'
    logger.info(log)
    
    return

##################################################
# 사용자 삭제(DELETE)
##################################################
def apptoasterDeleteUserHandler(request):
    # Logger
    ip = utilities.getIp(request)
    key = 'UNKNOWN'
    log = utilities.timestamp() + ' - '

    # request method 확인
    if request.method != 'DELETE':
        log += key + '(' + ip + ') - apptoasterDeleteUser() - error - request method error;'
        logger.warning(log)
        return json.dumps({
            'result':'request method error'
        })

    # GET 데이터 수신
    try:
        key = request.GET['key']
        user_id = request.GET['user_id']
    except:
        log += key + '(' + ip + ') - apptoasterDeleteUser() - error - required parameter error;'
        logger.warning(log)
        return json.dumps({
            'result':'required parameter error'
        })

    log += key + '(' + ip + ') - apptoasterDeleteUser() - delete user(' + user_id + ');'
    logger.info(log)
    
    return

##################################################
# 알림 메세지 송신(POST)
##################################################
def apptoasterSendNotificationToUserHandler(request):
    # Logger
    ip = utilities.getIp(request)
    key = 'UNKNOWN'
    log = utilities.timestamp() + ' - '

    # request method 확인
    if request.method != 'POST':
        log += key + '(' + ip + ') - apptoasterSendNotificationToUser() - error - request method error;'
        logger.warning(log)
        return json.dumps({
            'result':'request method error'
        })

    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
        key = request_dictionary['key']
        user_id = request_dictionary['user_id']
        title = request_dictionary['title']
        message = request_dictionary['message']
    except:
        log += key + '(' + ip + ') - apptoasterSendNotificationToUser() - error - json decode error;'
        logger.warning(log)
        return json.dumps({
            'result':'json decode error'
        })

    log += key + '(' + ip + ') - apptoasterSendNotificationToUser() - notification has sent to user(' + user_id + ');'
    logger.info(log)
    
    return

##################################################
# 전체 알림 메세지 송신(POST)
##################################################
def apptoasterSendNotificationToAllHandler(request):
    # Logger
    ip = utilities.getIp(request)
    key = 'UNKNOWN'
    log = utilities.timestamp() + ' - '

    # request method 확인
    if request.method != 'POST':
        log += key + '(' + ip + ') - apptoasterSendNotificationToAll() - error - request method error;'
        logger.warning(log)
        return json.dumps({
            'result':'request method error'
        })

    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
        key = request_dictionary['key']
        title = request_dictionary['title']
        message = request_dictionary['message']
    except:
        log += key + '(' + ip + ') - apptoasterSendNotificationToAll() - error - json decode error;'
        logger.warning(log)
        return json.dumps({
            'result':'json decode error'
        })

    log += key + '(' + ip + ') - apptoasterSendNotificationToAll() - notification has sent to all;'
    logger.info(log)
    
    return

##################################################
# 카카오 PUSH API(TEST)
##################################################
##################################################
# 푸시 토큰 등록하기
##################################################
def kakaoRegisterPushTokenHandler(request):
    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
    except:
        request_dictionary = ""

    # GET 데이터 수신
    kakao_app_admin_key = request.GET.get("kakao_app_admin_key")
    uuid = request.GET.get("uuid")
    device_id = request.GET.get("device_id")
    push_type = request.GET.get("push_type")
    push_token = request.GET.get("push_token")

    return utilities.kakaoRegisterPushToken(kakao_app_admin_key, uuid, device_id, push_type, push_token)

##################################################
# 푸시 토큰 보기
##################################################
def kakaoGetPushTokenHandler(request):
    # POST 데이터 kakaoGetPushTokenHandler
    try:
        request_dictionary = json.loads(request.body)
    except:
        request_dictionary = ""

    # GET 데이터 수신
    kakao_app_admin_key = request.GET.get("kakao_app_admin_key")
    uuid = request.GET.get("uuid")

    return utilities.kakaoGetPushToken(kakao_app_admin_key, uuid)

##################################################
# 푸시 토큰 삭제하기
##################################################
def kakaoDeletePushTokenHandler(request):
    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
    except:
        request_dictionary = ""

    # GET 데이터 수신
    kakao_app_admin_key = request.GET.get("kakao_app_admin_key")
    uuid = request.GET.get("uuid")
    device_id = request.GET.get("device_id")
    push_type = request.GET.get("push_type")

    return utilities.kakaoDeletePushToken(kakao_app_admin_key, uuid, device_id, push_type)

##################################################
# 푸시 알림 보내기
##################################################
def kakaoSendPushNotificationHandler(request):
    # POST 데이터 수신
    try:
        request_dictionary = json.loads(request.body)
    except:
        request_dictionary = ""

    # GET 데이터 수신
    kakao_app_admin_key = request.GET.get("kakao_app_admin_key")
    title = request.GET.get("title")
    message = request.GET.get("message")
    uuid_list = []
    uuid_list.append(request.GET.get("uuid"))

    return utilities.kakaoSendPushNotification(kakao_app_admin_key, title, message, uuid_list)