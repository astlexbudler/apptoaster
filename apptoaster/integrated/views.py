from django.shortcuts import render
from django.http import HttpResponse
from .handlers import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
import logging
import datetime

logger = logging.getLogger('appToaster')

##################################################
# 웹 페이지 경로
##################################################
# 메인 페이지
def webIndex(request):
    return render(request, "index.html")

# 서비스 이용 약관
def webPushPolicy(request):
    return render(request, "policy.html")

# 발송 관리 페이지
def webPushToasting(request):
    return render(request, "toasting.html")

# 발송 기록 페이지
def webPushToasted(request):
    return render(request, "toasted.html")

# 내부 테스트 페이지
def webTestConsole(request):
    return render(request, "test_console.html")

##################################################
# 앱 토스터 API
##################################################
# 수신인 관리(PUT/GET/PATCH)
@csrf_exempt
def apiTarget(request, key):
    try:
        userInfo = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'PUT':
            json = apiPutTargetHandler(request, userInfo)
        elif request.method == 'GET':
            json = apiGetTargetHandler(request, userInfo)
        elif request.method == 'PATCH':
            json = apiPatchTargetHandler(request, userInfo)
    except:
        json = ''
    
    return HttpResponse(json)

# 로그인
@csrf_exempt
def apiLogin(request, key):
    return HttpResponse()

# 로그아웃
@csrf_exempt
def apiLogout(request):
    return HttpResponse()

# 내부 테스트 API
@csrf_exempt
def apiTest(request):
    return HttpResponse()

##################################################
# PUSH API
##################################################
# PUSH 스케줄 추가(POST)
@csrf_exempt
def apiToastPush(request, key):
    try:
        userInfo = USER_TABLE.objects.get(
            key = key
        )
        if request.method == 'POST':
            json = apiToastPushHandler(request, userInfo)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 수정(POST)
@csrf_exempt
def apiUpdatePush(request, key):
    try:
        userInfo = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'POST':
            json = apiUpdatePushHandler(request, userInfo)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 스케줄 확인/삭제(GET/DELETE)
@csrf_exempt
def apiPush(request, key):
    try:
        json = ''
        user_info = USER_TABLE.objects.get(
            key = key
        )
        if request.method == 'GET':
            json = apiGetPushHandler(request, user_info)
        elif request.method == 'DELETE':
            json = apiDeletePushHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 기록 확인(GET)
@csrf_exempt
def apiPushToasted(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'GET':
            json = apiPushToastedHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)



##################################################
# CIA(ChurchInApp) API
##################################################
# 수신인 관리(PUT/GET/PATCH/DELETE)
@csrf_exempt
def ciaTarget(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )

        if request.method == 'PUT':
            json = ciaPutTargetHandler(request, user_info)
        elif request.method == 'GET':
            json = ciaGetTargetHandler(request, user_info)
        elif request.method == 'PATCH':
            json = ciaPatchTargetHandler(request, user_info)
        elif request.method == 'DELETE':
            json = ciaDeleteTargetHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 스케줄 추가(POST)
@csrf_exempt
def ciaToastPush(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'POST':
            json = ciaToastPushHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 수정(POST)
@csrf_exempt
def ciaUpdatePush(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'POST':
            json = ciaUpdatePushhandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 스케줄 확인/삭제(GET/DELETE)
@csrf_exempt
def ciaPush(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )

        if request.method == 'GET':
            json = ciaGetPushHandler(request, user_info)
        elif request.method == 'DELETE':
            json = ciaDeletePushHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# PUSH 기록 확인(GET)
@csrf_exempt
def ciaPushToasted(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'GET':
            json = ciaPushToasted(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)



##################################################
# POPUP API
##################################################
# POPUP 스케줄 추가(POST)
@csrf_exempt
def apiToastPopup(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'POST':
            json = apiToastPopupHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# POPUP 수정(POST)
@csrf_exempt
def apiUpdatePopup(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'POST':
            json = apiUpdatePopupHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# POPUP 스케줄 확인/삭제(GET/DELETE)
@csrf_exempt
def apiPopup(request, key):
    try:
        json = ''
        user_info = USER_TABLE.objects.get(
            key = key
        )
        if request.method == 'GET':
            json = apiGetPopupHandler(request, user_info)
        elif request.method == 'DELETE':
            json = apiDeletePopupHandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)

# POPUP 기록 확인(GET)
@csrf_exempt
def apiPopupToasted(request, key):
    try:
        user_info = USER_TABLE.objects.get(
            key = key
        )        
        if request.method == 'GET':
            json = apiPopupToastedhandler(request, user_info)
    except:
        json = ''
    
    return HttpResponse(json)