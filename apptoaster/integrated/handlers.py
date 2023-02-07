import json
import math
from .models import *
from .services import api
from .services import common
from .services import email
from .services import model
from .services import session

import logging
logger = logging.getLogger('appToaster')

##################################################
# 웹 페이지 경로
##################################################
##################################################
# 계정 관리 페이지
##################################################
def webToasterHandler(request):
    try:
        toaster = model.readToaster(request.GET['key'])

        return {
            "toaster": toaster
        }

    except:
        return

##################################################
# PUSH 발송 관리 페이지
##################################################
def webPushToastingHandler(request):
    try:
        toaster = model.readToaster(request.GET['key'])
        pushList = model.readPush(toaster['id'])

        return {
            "toaster": toaster,
            "pushList": pushList
        }

    except:
        return

##################################################
# PUSH 발송 기록 페이지
##################################################
def webPushToastedHandler(request):
    try:
        logger.debug(1)
        toaster = model.readToaster(request.GET['key'])

        pushList = model.readPushHistory(toaster['id'])
        read = 100
        page = int(request.GET.get('page', '1')) - 1
        lastPage = math.floor(len(pushList) / 100)
        if page > lastPage:
            page = lastPage

        logger.debug(pushList)
        index = 0
        _pushList = []
        for push in pushList:
            if (index >= read * page) & (index < read * (page + 1)):
                _pushList.append(push)
            index = index + 1

        logger.debug(3)
        return {
            "toaster": toaster,
            'page': {
                'now': page + 1,
                'lastPage': lastPage + 1
            },
            "pushList": _pushList
        }

    except:
        return

##################################################
# 관리자 페이지
##################################################
def webOverseerHandler(request):
    try:
        function = request.POST['function']
        if function == 'send_jobs_done':
            key = request.POST['key']
            toaster = model.readToaster(key)
            applicationName = toaster['applicationName']
            expireDate = common.dateToString(toaster['expireDate'])
            iconUrl = 'https://apptoaster.co.kr/media/icons/' + toaster['id'] + '.png'
            to = toaster['email']
            url = request.POST['url']
            designNote = request.POST['designNote']
            downloadLink = request.POST['downloadLink']
            
            html = email.jobsDone(iconUrl, applicationName, url, designNote, expireDate, downloadLink, key)
            email.sendEmail(to, '[앱 토스터] 어플리케이션 변환 작업이 완료되었습니다.', html)

        elif function == 'send_email_tools_to':
            key = request.POST['key']
            toaster = model.readToaster(key)
            applicationName = toaster['applicationName']
            to = toaster['email']

            html = email.emailPushTool(applicationName, key)
            email.sendEmail(to, '[앱 토스터] PUSH 메세지 관리자 1.0', html)

        elif function == 'send_email_tools_to_all':
            toasterList = model.readToasterAll()
            for toaster in toasterList:
                toaster = model.readToaster(key)
                key = toaster['key']
                applicationName = toaster['applicationName']

                html = email.emailPushTool(applicationName, key)
                email.sendEmail(to, '[앱 토스터] PUSH 메세지 관리자 1.1', html)

    except:
        return
        


##################################################
# 앱 토스터 API
##################################################
##################################################
# 수신인 확인(없을경우 생성)
##################################################
def apiGetTargetHandler(request, toaster):
    try:
        if toaster == None:
            raise Exception()

        deviceType = request.GET['deviceType']
        token = request.GET['token']
        target = model.readTarget(deviceType, token)

        # 없을경우 생성
        if target == None:
            model.createTarget(toaster['id'], deviceType, token)
            target = model.readTarget(deviceType, token)
            return json.dumps({
                'status': 'new',
                'target': target
            })

        return json.dumps({
            'status': 'exist',
            'target': target
        })
    except:
        return json.dumps({
            'status': "denied",
            'target': None
        })

##################################################
# 수신인 수정
##################################################
def apiPatchTargetHandler(request):
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

        model.updateTarget(id, isPushAllow, isAdAllow)

        return
    except:
        return

##################################################
# PUSH API
##################################################
##################################################
# PUSH 스케줄 추가(POST)
##################################################
def apiToastPushHandler(request, toaster):
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
            
        model.createPush(toaster['id'], alias, title, message, date, time, repeat, ad)

        return '/toast_push_success'
    except:
        return '/toast_push_fail'

##################################################
# PUSH 수정
##################################################
def apiUpdatePushHandler(request, toasterInfo):
    try:
        id = request.POST.get('id', '')
        alias = request.POST['alias']
        title = request.POST['title']
        message = request.POST['message']
        if request.POST["date"] == 'null':
            date = ''
        else:
            date = request.POST["date"]
        if request.POST["time"] == 'null':
            time = ''
        else:
            time = request.POST["time"]
        date = common.stringToDate(date)
        time = common.stringToTime(time)
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
        
        if id == '':
            model.updatePushAlias(alias, toasterInfo.id, title, message, date, time, repeat, ad)
        else:
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
def apiGetPushHandler(request, toasterInfo):
    try:
        pushList = model.readPush(toasterInfo.id)

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
def apiDeletePushHandler(request, toasterInfo):
    try:
        id = request.GET.get('id', '')
        if id == '':
            alias = request.GET.get('alias', '')
            model.deletePushAlias(alias)
        else:
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
def apiPushToastedHandler(request, toasterInfo):
    try:
        pushList = model.readPushHistory(toasterInfo.id)

        return json.dumps({
            'isSucceed': True,
            'pushList': pushList
        })
    except:
        return json.dumps({
            'isSucceed': False,
            'pushList': None
        })