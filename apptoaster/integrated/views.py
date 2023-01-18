from django.shortcuts import render
from django.http import HttpResponse
from . import handlers

##################################################
# Web
##################################################
def index(request):
    return render(request, "appToaster/index.html")

def test(request):
    return render(request, "appToaster/test.html")

##################################################
# 앱 토스터 API
##################################################
def apptoasterSetUser(request):
    return HttpResponse(handlers.apptoasterSetUserHandler(request))

def apptoasterGetUser(request):
    return HttpResponse(handlers.apptoasterGetUserHandler(request))

def apptoasterDeleteUser(request):
    return HttpResponse(handlers.apptoasterDeleteUserHandler(request))

def apptoasterSendNotificationToUser(request):
    return HttpResponse(handlers.apptoasterSendNotificationToUserHandler(request))

def apptoasterSendNotificationToAll(request):
    return HttpResponse(handlers.apptoasterSendNotificationToAllHandler(request))

##################################################
# 카카오 PUSH API(TEST)
##################################################
def kakaoRegisterPushToken(request):
    return HttpResponse(handlers.kakaoRegisterPushTokenHandler(request))

def kakaoGetPushToken(request):
    return HttpResponse(handlers.kakaoGetPushTokenHandler(request))

def kakaoDeletePushToken(request):
    return HttpResponse(handlers.kakaoDeletePushTokenHandler(request))

def kakaoSendPushNotification(request):
    return HttpResponse(handlers.kakaoSendPushNotificationHandler(request))