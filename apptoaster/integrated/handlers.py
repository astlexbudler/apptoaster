import json
from .services import api
from .services import common
from .services import email
from .services import model
from .services import session

import logging
logger = logging.getLogger('appToaster')

##################################################
# 수신인 등록
##################################################
def apiPutTargetHandler(request, userInfo):
    try:
        deviceType = request.GET['deviceType']
        token = request.GET['token']
        isPushAllow = request.GET['isPushAllow']
        if isPushAllow == 'true':
            isPushAllow = True
        else:
            isPushAllow = False

        model.createTarget(userInfo.id, deviceType, token, isPushAllow)

        return json.dumps({
            'isSucceed': True
        })
    except:
        return json.dumps({
            'isSucceed': False
        })

##################################################
# 수신인 확인
##################################################
def apiGetTargetHandler(request, userInfo):
    try:
        deviceType = request.GET['deviceType']
        token = request.GET['token']

        targetInfo = model.readTarget(deviceType, token)

        return json.dumps({
            'isSucceed': True,
            'targetInfo': targetInfo
        })
    except:
        return json.dumps({
            'isSucceed': False,
            'targetInfo': None
        })

##################################################
# 수신인 수정
##################################################
def apiPatchTargetHandler(request, userInfo):
    try:
        id = request.GET['id']
        isPushAllow = request.GET['isPushAllow']
        if isPushAllow == 'true':
            isPushAllow = True
        else:
            isPushAllow = False
        isAdAllow = request.GET['isAdAllow']
        if isAdAllow == 'true':
            isAdAllow = True
        else:
            isAdAllow = False
        isNightAllow = request.GET['isNightAllow']
        if isNightAllow == 'true':
            isNightAllow = True
        else:
            isNightAllow = False

        model.updateTarget(id, isPushAllow, isAdAllow, isNightAllow)

        return json.dumps({
            'isSucceed': True
        })
    except:
        return json.dumps({
            'isSucceed': False
        })

##################################################
# PUSH API
##################################################
##################################################
# PUSH 스케줄 추가(POST)
##################################################
def apiToastPushHandler(request, userInfo):
    try:
        alias = request.POST['alias']
        title = request.POST['title']
        message = request.POST['message']
        date = common.stringToDate(request.POST.get('date', ''))
        time = common.stringToTime(request.POST.get('time', ''))
        repeat = request.POST['repeat']
        if repeat == '2':
            repeat = True
        else:
            repeat = False
        ad = request.POST['ad']
        if ad == '1':
            ad = True
        else:
            ad = False

        model.createPush(userInfo.id, alias, title, message, date, time, repeat, ad)

        return json.dumps({
            'isSucceed': True
        })
    except:
        return json.dumps({
            'isSucceed': False
        })

##################################################
# PUSH 수정
##################################################
def apiUpdatePushHandler(request, userInfo):
    try:
        id = request.POST['id']
        alias = request.POST['alias']
        title = request.POST['title']
        message = request.POST['message']
        date = common.stringToDate(request.POST.get('date', ''))
        time = common.stringToTime(request.POST.get('time', ''))
        repeat = request.POST['repeat']
        if repeat == '2':
            repeat = True
        else:
            repeat = False
        ad = request.POST['ad']
        if ad == '1':
            ad = True
        else:
            ad = False

            model.updatePush(id, alias, title, message, date, time, repeat, ad)

        return json.dumps({
            'isSucceed': True
        })
    except:
        return json.dumps({
            'isSucceed': False
        })

##################################################
# PUSH 스케줄 확인
##################################################
def apiGetPushHandler(request, userInfo):
    try:
        pushList = model.readPush(userInfo.id)

        return json.dumps({
            'isSucceed': True,
            'pushList': pushList
        })
    except:
        return json.dumps({
            'isSucceed': False,
            'pushList': None
        })

##################################################
# PUSH 삭제
##################################################
def apiDeletePushHandler(request, userInfo):
    try:
        id = request.GET['id']

        model.deletePush(id)

        return json.dumps({
            'isSucceed': True
        })
    except:
        return json.dumps({
            'isSucceed': False
        })


##################################################
# PUSH 기록 확인
##################################################
def apiPushToastedHandler(request, userInfo):
    try:
        pushList = model.readPushHistory(userInfo.id)

        return json.dumps({
            'isSucceed': True,
            'pushList': pushList
        })
    except:
        return json.dumps({
            'isSucceed': False,
            'pushList': None
        })