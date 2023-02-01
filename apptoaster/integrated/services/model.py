from ..models import *
from . import common

import logging
logger = logging.getLogger('appToaster')

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
        logger.info('services.model.createSystemLog 시스템 기록 생성 실패.' + e)

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
def readToaster(key):
    try:
        toaster = TOASTER_TABLE.objects.get(
            key = key
        )
        
        if len(toaster.application_name) > 16:
            applicationShortName = toaster.application_name[0:16] + '..'
        else:
            applicationShortName = toaster.application_name
        
        return {
            'id': toaster.id,
            'key': toaster.key,
            'applicationIcon': '/media/icons/' + toaster.id + '.png',
            'applicationName': toaster.application_name,
            'applicationShortName': applicationShortName,
            'email': toaster.email,
            'tel': toaster.tel,
            'appAdminKey': toaster.app_admin_key,
            'createDate': toaster.create_date,
            'expireDate': toaster.expire_date,
        }

    except:
        return

# 앱 토스터 고객 확인
def readToasterById(id):
    try:
        toaster = TOASTER_TABLE.objects.get(
            id = id
        )
        
        return {
            'id': toaster.id,
            'key': toaster.key,
            'applicationIcon': '/media/icons/' + toaster.id + '.png',
            'applicationName': toaster.application_name,
            'email': toaster.email,
            'tel': toaster.tel,
            'appAdminKey': toaster.app_admin_key,
            'createDate': toaster.create_date,
            'expireDate': toaster.expire_date,
        }

    except:
        return

# 앱 토스터 고객 목록
def readToasterAll():
    try:
        toasterList = TOASTER_TABLE.objects.all()

        list = []
        for toaster in toasterList:
            list.append({
            'id': toaster.id,
            'key': toaster.key,
            'applicationIcon': '/media/icons/' + toaster.id + '.png',
            'applicationName': toaster.application_name,
            'email': toaster.email,
            'tel': toaster.tel,
            'appAdminKey': toaster.app_admin_key,
            'createDate': toaster.create_date,
            'expireDate': toaster.expire_date,
        })
        
        return list

    except:
        return

##################################################
# 앱 사용자 테이블
##################################################
# 앱 사용자 생성
def createTarget(toasterId, deviceType, token, isPushAllow):
    try:
        nowDate = common.stringToDate('')
        nowDatetime = common.stringToDatetime('')
        id = common.getId()

        TARGET_TABLE(
            id = id,
            token = token,
            toaster_id = toasterId,
            device_type = deviceType,
            is_push_allow = isPushAllow,
            push_allow_datetime = nowDatetime,
            is_ad_allow = False,
            ad_allow_datetime = nowDatetime,
            is_night_allow = False,
            night_allow_datetime = nowDatetime,
            last_active_date = nowDate
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
            token = target.token,
            toaster_id = target.toaster_id,
            device_type = target.device_type,
            is_push_allow = target.is_push_allow,
            push_allow_datetime = target.push_allow_datetime,
            is_ad_allow = target.is_ad_allow,
            ad_allow_datetime = target.ad_allow_datetime,
            last_active_date = nowDate
        ).save()
        
        return {
            'id': target.id,
            "token": target.token,
            "toasterId": target.toaster_id,
            "deviceType": target.device_type,
            "isPushAllow": target.is_push_allow,
            'pushAllowDatetime': common.datetimeToString(target.push_allow_datetime),
            "isAdAllow": target.is_ad_allow,
            "adAllowDatetime": common.datetimeToString(target.ad_allow_datetime),
            "lastActiveDate": common.dateToString(target.last_active_date)
        }
    
    except:
        return

# 사용자의 타겟 모두 확인
def readToasterTarget(toasterId):
    try:
        targetList = TARGET_TABLE.objects.all().filter(
            toaster_id = toasterId
        )
        
        list = []
        for target in targetList:
            list.append({
            'id': target.id,
            "token": target.token,
            "toasterId": target.toaster_id,
            "deviceType": target.device_type,
            "isPushAllow": target.is_push_allow,
            'pushAllowDatetime': common.datetimeToString(target.push_allow_datetime),
            "isAdAllow": target.is_ad_allow,
            "adAllowDatetime": common.datetimeToString(target.ad_allow_datetime),
            "isNightAllow": target.is_night_allow,
            'nightAllowDatetime': common.datetimeToString(target.night_allow_datetime),
            "lastActiveDate": common.dateToString(target.last_active_date)
        })
        
        return list
    
    except:
        return

# 앱 사용자 수정
def updateTarget(id, isPushAllow, isAdAllow):
    try:

        target = TARGET_TABLE.objects.get(
            id = id
        )

        nowDatetime = common.stringToDatetime('')
        if isPushAllow:
            pushAllowDatetime = nowDatetime
        else:
            pushAllowDatetime = target.push_allow_datetime
        if isAdAllow:
            adAllowDatetime = nowDatetime
        else:
            adAllowDatetime = target.ad_allow_datetime


        TARGET_TABLE(
            id = id,
            token = target.token,
            toaster_id = target.toaster_id,
            device_type = target.device_type,
            is_push_allow = isPushAllow,
            push_allow_datetime = pushAllowDatetime,
            is_ad_allow = isAdAllow,
            ad_allow_datetime = adAllowDatetime,
            last_active_date = target.last_active_date
        ).save()

        target = TARGET_TABLE.objects.get(
            id = id
        )

        return {
            'id': target.id,
            "token": target.token,
            "toasterId": target.toaster_id,
            "deviceType": target.device_type,
            "isPushAllow": target.is_push_allow,
            'pushAllowDatetime': common.datetimeToString(target.push_allow_datetime),
            "isAdAllow": target.is_ad_allow,
            "adAllowDatetime": common.datetimeToString(target.ad_allow_datetime),
            "lastActiveDate": common.dateToString(target.last_active_date)
        }
    
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
def createPush(toasterId, alias, title, message, date, time, repeat, ad):
    try:
        id = common.getId()
        
        SCHEDULED_PUSH_TABLE(
            id = id,
            toaster_id = toasterId,
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
def readPush(toasterId):
    try:
        pushList = SCHEDULED_PUSH_TABLE.objects.all().filter(
            toaster_id = toasterId
        )

        list = []
        for push in pushList:
            if push.repeat:
                date = ''
            else:
                date = common.dateToString(push.date)

            list.append({
                "id": push.id,
                "toasterId": push.toaster_id,
                "alias": push.alias,
                "title": push.title,
                "message": push.message,
                "date": date,
                "time": common.timeToString(push.time),
                "repeat": push.repeat,
                "ad": push.ad
            })

        return list

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.readPush PUSH 예약 확인 실패. ' + e)

# 모든 PUSH 예약 확인
def readPushAll():
    try:
        pushList = SCHEDULED_PUSH_TABLE.objects.all()

        list = []
        for push in pushList:
            list.append({
                "id": push.id,
                "toasterId": push.toaster_id,
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
        createSystemLog(9, 'SYSTEM', 'services.model.readPushAll PUSH 예약 확인 실패. ' + e)


# PUSH 예약 수정
def updatePush(id, alias, title, message, date, time, repeat, ad):
    try:
        push = SCHEDULED_PUSH_TABLE.objects.get(
            id = id
        )

        SCHEDULED_PUSH_TABLE(
            id = id,
            toaster_id = push.toaster_id,
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

# PUSH 예약 수정(alias)
def updatePushAlias(alias, toasterId, title, message, date, time, repeat, ad):
    try:
        push = SCHEDULED_PUSH_TABLE.objects.get(
            alias = alias,
            toasterId = toasterId
        )

        SCHEDULED_PUSH_TABLE(
            id = push.id,
            toaster_id = toasterId,
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

# PUSH 예약 삭제(alias)
def deletePushAlias(alias):
    try:
        SCHEDULED_PUSH_TABLE.objects.all().filter(
            alias = alias
        ).delete()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.deletePush PUSH 예약 삭제 실패. ' + e)


##################################################
# PUSH 기록
##################################################
# PUSH 기록 생성
def createPushHistory(toasterId, alias, title, message, repeat, ad, count):
    try:
        nowDatetime = common.stringToDatetime('')

        PUSH_HISTORY_TABLE(
            toaster_id = toasterId,
            alias = alias,
            title = title,
            message = message,
            toasted_datetime = nowDatetime,
            repeat = repeat,
            ad = ad,
            count = count
        ).save()
    
    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.createPushHistory PUSH 기록 생성 실패. ' + e)

# PUSH 기록 확인
def readPushHistory(toasterId):
    try:
        pushHistoryList = PUSH_HISTORY_TABLE.objects.all().filter(
            toaster_id = toasterId
        )

        list = []
        for pushHistory in pushHistoryList:
            list.append({
                "toasterId": pushHistory.toaster_id,
                "alias": pushHistory.alias,
                "title": pushHistory.title,
                "message": pushHistory.message,
                "toastedDatetime": common.datetimeToString(pushHistory.toasted_datetime),
                "repeat": pushHistory.repeat,
                "ad": pushHistory.ad,
                'count': pushHistory.count
            })

        return list

    except Exception() as e:
        createSystemLog(9, 'SYSTEM', 'services.model.getPushHistory PUSH 기록 확인 실패. ' + e)    