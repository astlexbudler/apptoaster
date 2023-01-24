from ..models import *
from . import common

'''
model.py
데이터베이스 관련 기능을 관리하는 서비스입니다.
'''

##################################################
# 시스템 기록 테이블
##################################################
# 시스템 기록 생성
def createSystemLog(level, applicationName, message):
    try:
        id = common.getId()

        SYSTEM_LOG_TABLE(
            id = id,
            level = level,
            application_name = applicationName,
            message = message,
        ).save()

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createSystemLog 시스템 기록 생성 실패. ' + e)

##################################################
# 로그인 관리 테이블
##################################################
# 로그인 관리 생성
def createLoginControl(ip):
    try:
        LOGIN_CONTROL_TABLE(
            ip = ip,
            count = 5
        ).save()

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createLoginControl 로그인 관리 테이블 생성 실패. ' + e)

# 로그인 관리 확인
def readLoginControl(ip):
    try:
        loginControl = LOGIN_CONTROL_TABLE.objects.get(
            ip = ip
        )

        return {
            'ip': loginControl.ip,
            'count': loginControl.count
        }

    except:
        return

# 로그인 관리 수정
def updateLoginControl(ip, count):
    try:
        LOGIN_CONTROL_TABLE(
            ip = ip,
            count = count
        ).save()
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.updateLoginControl 로그인 관리 테이블 수정 실패. ' + e)

# 로그인 관리 초기화
def initLoginControl():
    try:
        LOGIN_CONTROL_TABLE.objects.all().delete()

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.updateLoginControl 로그인 관리 테이블 초기화 실패. ' + e)

##################################################
# 앱 토스터 고객 테이블
##################################################
# 앱 토스터 고객 확인
def readUser(key):
    try:
        user = USER_TABLE.objects.get(
            key = key
        )

        if len(user['application_name']) > 16:
            applicationShortName = user['application_name'][0:16] + '..'
        else:
            applicationShortName = user['application_name']

        emailList = USER_EMAIL_TABLE.objects.all().filter(
            user_id = user.id
        )

        list = []
        for email in emailList:
            list.append(email.email)
        emailList = list

        return {
            'id': user.id,
            'key': user.key,
            'applicationIcon': '/media/icons/' + user.id + '.png',
            'applicationName': user.application_name,
            'applicationShortName': applicationShortName,
            'tel': user.tel,
            'serviceId': user.service_id,
            'accessKey': user.access_key,
            'secretKey': user.secret_key,
            'expireDate': user.expire_date,
            'email': emailList
        }

    except:
        return

##################################################
# 앱 사용자 테이블
##################################################
# 앱 사용자 생성
def createTarget(userId, deviceType, token, isPushAllow):
    try:
        nowDate = common.stringToDate('')
        id = common.getId()

        TARGET_TABLE(
            id = id,
            token = token,
            user_id = userId,
            device_type = deviceType,
            is_push_allow = isPushAllow,
            is_ad_allow = False,
            is_night_allow = False,
            last_active_date = nowDate,
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createTarget 앱 사용자 생성 실패. ' + e)

# 앱 사용자 확인
def readTarget(deviceType, token):
    try:
        nowDate = common.stringToDate('')

        target = TARGET_TABLE.objects.get(
            device_type = deviceType,
            token = token
        )

        TARGET_TABLE(
            id = target.id,
            last_active_date = nowDate
        ).save()

        return {
            'id': target.id,
            "token": target.token,
            "userId": target.user_id,
            "deviceType": target.device_type,
            "isPushAllow": target.is_push_allow,
            "isAdAllow": target.is_ad_allow,
            "isNightAllow": target.is_night_allow,
            "last_active_date": target.last_active_date
        }
    
    except:
        return

# 앱 사용자 수정
def updateTarget(id, isPushAllow, isAdAllow, isNightAllow):
    try:
        TARGET_TABLE(
            id = id,
            is_push_allow = isPushAllow,
            is_ad_allow = isAdAllow,
            is_night_allow = isNightAllow,
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.updateTarget 앱 사용자 수정 실패. ' + e)

# 앱 사용자 삭제
def deleteTarget(id):
    try:
        TARGET_TABLE.objects.get(
            id = id
        ).delete()

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.deleteTarget 앱 사용자 삭제 실패. ' + e)

##################################################
# PUSH 예약 테이블
##################################################
# PUSH 예약 생성
def createPush(userId, alias, title, message, date, time, repeat, ad):
    try:
        id = common.getId()

        SCHEDULED_PUSH_TABLE(
            id = id,
            user_id = userId,
            alias = alias,
            title = title,
            message = message,
            date = date,
            time = time,
            repeat = repeat,
            ad = ad
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createPush PUSH 예약 생성 실패. ' + e)

# PUSH 예약 확인
def readPush(userId):
    try:
        pushList = SCHEDULED_PUSH_TABLE.objects.all().filter(
            user_id = userId
        )

        list = []
        for push in pushList:
            list.append({
                "id": push.id,
                "userId": push.user_id,
                "alias": push.alias,
                "title": push.title,
                "message": push.message,
                "date": push.date,
                "time": push.time,
                "repeat": push.repeat,
                "ad": push.ad
            })

        return list

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.readPush PUSH 예약 확인 실패. ' + e)

# PUSH 예약 수정
def updatePush(id, alias, title, message, date, time, repeat, ad):
    try:
        SCHEDULED_PUSH_TABLE(
            id = id,
            alias = alias,
            title = title,
            message = message,
            date = date,
            time = time,
            repeat = repeat,
            ad = ad
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.updatePush PUSH 예약 수정 실패. ' + e)

# PUSH 예약 삭제
def deletePush(id):
    try:
        SCHEDULED_PUSH_TABLE.objects.get(
            id = id
        ).delete()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.deletePush PUSH 예약 삭제 실패. ' + e)

##################################################
# PUSH 기록
##################################################
# PUSH 기록 생성
def createPushHistory(userId, alias, title, message, date, time, repeat, ad):
    try:
        nowDatetime = common.stringToDatetime('')

        PUSH_HISTORY_TABLE(
            user_id = userId,
            alias = alias,
            title = title,
            message = message,
            toasted_datetime = nowDatetime,
            repeat = repeat,
            ad = ad
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createPushHistory PUSH 기록 생성 실패. ' + e)

# PUSH 기록 확인
def readPushHistory(userId):
    try:
        pushHistoryList = PUSH_HISTORY_TABLE.objects.all().filter(
            user_id = userId
        )

        list = []
        for pushHistory in pushHistoryList:
            list.append({
                "userId": pushHistory.user_id,
                "alias": pushHistory.alias,
                "title": pushHistory.title,
                "message": pushHistory.message,
                "toastedDatetime": pushHistory.toasted_datetime,
                "repeat": pushHistory.repeat,
                "ad": pushHistory.ad
            })

        return list

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.getPushHistory PUSH 기록 확인 실패. ' + e)    