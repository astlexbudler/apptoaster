from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import datetime
from .handlers import *
from .services import model

logger = logging.getLogger('appToaster')

##################################################
# 웹 페이지 경로
##################################################
# 메인 페이지
def webIndex(request):
    return render(request, "index.html")

# 계정 관리 페이지
def webToaster(request):
    try:
        toaster = model.readToaster(request.GET['key'])
        if toaster == None:
            raise Exception()

        return render(request, "toaster.html", webToasterHandler(request))

    except:
        return render(request, '404.html')

# PUSH 발송 관리 페이지
def webPushToasting(request):
    try:
        toaster = model.readToaster(request.GET['key'])
        if toaster == None:
            raise Exception()

        return render(request, "push_toasting.html", webPushToastingHandler(request))
        
    except:
        return render(request, '404.html')

# PUSH 발송 기록 페이지
def webPushToasted(request):
    try:
        toaster = model.readToaster(request.GET['key'])
        if toaster == None:
            raise Exception()

        return render(request, "push_toasted.html", webPushToastedHandler(request))
        
    except:
        return render(request, '404.html')

# 관리자 페이지
def webOverseer(request):
    try:
        toaster = model.readToaster(request.GET['key'])
        if toaster['id'] != '0':
            raise Exception()

        return render(request, "overseer.html", webOverseerHandler(request))
        
    except:
        return render(request, '404.html')

# 이용약관
def webPolicy(request):
    return render(request, "toasted.html")

# 개인정보 처리 방침
def webPrivacy(request):
    return render(request, "toasted.html")

# 내부 테스트 페이지
def webTest(request):
    return render(request, "test.html")

##################################################
# 앱 토스터 API
##################################################
# 수신인 관리(PUT/GET/PATCH)
@csrf_exempt
def apiTarget(request, key):
    try:
        toaster = model.readToaster(key)
        if toaster == None:
            raise Exception()

        if request.method == 'PUT':
            json = apiPutTargetHandler(request, toaster)
        elif request.method == 'GET':
            json = apiGetTargetHandler(request, toaster)
        elif request.method == 'PATCH':
            json = apiPatchTargetHandler(request, toaster)
    except:
        json = ''
    
    return HttpResponse(json)

# 이메일 관리 도구 발송
def apiSendEmailTools(request):
    return HttpResponse()

# 내부 테스트 API
@csrf_exempt
def apiTest(request):
    date = common.stringToDate('2020-01-01')
    time = common.stringToTime('24:00:00')

    return HttpResponse(datetime.datetime.combine())

##################################################
# PUSH API
##################################################
# PUSH 스케줄 추가(POST)
@csrf_exempt
def apiToastPush(request, key):
    try:
        toaster = model.readToaster(key)
        if toaster == None:
            raise Exception()

        if request.method == 'POST':
            json = apiToastPushHandler(request, toaster)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 수정(POST)
@csrf_exempt
def apiUpdatePush(request, key):
    try:
        toaster = model.readToaster(key)
        if toaster == None:
            raise Exception()

        if request.method == 'POST':
            json = apiUpdatePushHandler(request, toaster)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 스케줄 확인/삭제(GET/DELETE)
@csrf_exempt
def apiPush(request, key):
    try:
        toaster = model.readToaster(key)
        if toaster == None:
            raise Exception()

        if request.method == 'GET':
            json = apiGetPushHandler(request, toaster)
        elif request.method == 'DELETE':
            json = apiDeletePushHandler(request, toaster)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 기록 확인(GET)
@csrf_exempt
def apiPushToasted(request, key):
    try:
        toaster = model.readToaster(key)
        if toaster == None:
            raise Exception()

        if request.method == 'GET':
            json = apiPushToastedHandler(request, toaster)
    except:
        json = ''
    
    return HttpResponse(json)