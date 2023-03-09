from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from . import handlers
from .services import model
from .services import session
from .services import common
from .services import api
from . import models
import requests
import json
import logging
logger = logging.getLogger('appToaster')

##################################################
# 웹 페이지 경로
##################################################
########################################
# 메인
########################################
def index(request):
    return render(request, "index.html")

########################################
# 템플릿
########################################
def template(request):
    return render(request, "template.html")

########################################
# 이용약관
########################################
def policy(request):
    return render(request, "policy.html")

########################################
# 개인정보 처리방침
########################################
def privacy(request):
    return render(request, "privacy.html")



##################################################
# 앱 관리
##################################################
########################################
# 로그인
########################################
def login(request):
    user = model.getUser(session.getId(request))
    if user != None:
        return redirect('/dash')
    return render(request, "login.html")

def apiLogin(request):
    return HttpResponse(json.dumps(handlers.apiLogin(request)))

def apiLogout(request):
    return HttpResponse(json.dumps(handlers.apiLogout(request)))

########################################
# 대시보드
########################################
def dash(request):
    context = handlers.dash(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "dash.html", context)

########################################
# 푸시 관리
########################################
def push(request):
    context = handlers.push(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "push.html", context)

########################################
# 일반 설정
########################################
def general(request):
    context = handlers.general(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "general.html", context)

def generalUpdate(request):
    context = handlers.generalUpdate(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "general_update.html", context)

def apiGeneralUpdate(request):
    return HttpResponse(handlers.apiGeneralUpdate(request))

########################################
# 로딩 설정
########################################
def splash(request):
    context = handlers.splash(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "splash.html", context)

########################################
# 레이아웃 설정
########################################
def layout(request):
    context = handlers.layout(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "layout.html", context)

########################################
# 질문하기
########################################
def faq(request):
    context = handlers.faq(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "faq.html", context)

def qna(request):
    context = handlers.qna(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "qna.html", context)

def apiQnaCreate(request):
    handlers.apiQnaCreate(request)
    return HttpResponse()

########################################
# 접속 기록
########################################
def accessLog(request):
    context = handlers.accessLog(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "access_log.html", context)

########################################
# 업데이트 기록
########################################
def updateLog(request):
    context = handlers.updateLog(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "update_log.html", context)



##################################################
# 앱 토스터 API
##################################################
########################################
# 타겟 관리(GET/PATCH)
########################################
@csrf_exempt
def apiTarget(request, id):

    if request.method == 'GET':
        json = handlers.apiGetTarget(request, id)
    elif request.method == 'PATCH':
        json = handlers.apiPatchTarget(request, id)

    return HttpResponse(json)

########################################
# 타겟 관리(GET/POST)
########################################
@csrf_exempt
def apiId(request):
    list = []
    for i in range(100):
        list.append(common.id() + '<br>')
    
    return HttpResponse(list)

########################################
# 테스트
########################################
@csrf_exempt
def apiTest(request):
    return HttpResponse(api.kakaoGetTarget('a976cf90d58cb928f781590a77461fcd','2402615545658066410'))



##################################################
# 푸시
##################################################
########################################
# 푸시 관리(POST/DELETE)
########################################
@csrf_exempt
def apiPush(request, id):
    try:
        user = model.getUser(id)

        if user == None:
            raise Exception()

        if request.method == 'POST':
            url = handlers.apiPostPush(request, user)
        if request.method == 'DELETE':
            url = handlers.apiDeletePush(request, user)

    except:
        url = 'toast_push_fail.html'
    
    return render(request, url)

##################################################
# EVERYPUSH ORIGINAL
##################################################
########################################
# 에브리푸시 이용약관 및 개인정보처리방침
########################################
def everypushTerms(request):
    return render(request, 'everypush_terms.html')

########################################
# 유저 부가정보(ADDITIONAL USER DATA)
########################################
@csrf_exempt
def everypushGetAdditionalData(request):
    return HttpResponse(handlers.getAdditionalUserData(request))

########################################
# 결제페이지
########################################
def everypushPayments(request):
    context = handlers.dash(request)

    if context['user'] == None:
        return redirect("/login")
    
    return render(request, "everypush_payments.html", context)

########################################
# 결제결과페이지(임시)
########################################
def everypushPaymentsResult(request):
    return render(request, 'everypush_payments_result.html')

########################################
# 일반결제 성공
########################################
def everypushPaymentsSuccess(request):
    result_dict = handlers.paymentsSuccessHandler(request)
    if result_dict["result"] == "200":
        context = {
            "status":"success",
            "result_dict":result_dict
        }
    else:
        context = {
            "status":"error",
            "result_dict":result_dict
        }
    return render(request, 'everypush_payments_result.html', context)
    
########################################
# 일반결제 실패(서버외부요인)
########################################
def everypushPaymentsFail(request):
    context = {"status":"fail"}
    return render(request, 'everypush_payments_result.html', context)

########################################
# 빌링 성공 = 연동성공, 결제 시도.
########################################
def everypushBillingSuccess(request):
    result_dict = handlers.billingSuccessHandler(request)
    result_dict = handlers.billingPaymentsHandler(request)
    if result_dict["result"] == "200":
        context = {
            "status":"success",
            "result_dict":result_dict
        }
    else:
        context = {
            "status":"error",
            "result_dict":result_dict
        }
    return render(request, 'everypush_payments_result.html', context)

########################################
# 빌링결제 실패(서버외부요인)
########################################
def everypushBillingFail(request):
    context = {"status":"fail"}
    return render(request, 'everypush_payments_result.html', context)

########################################
# 빌링 연장
########################################
def everypushRenewBilling(request):
    result_dict = handlers.billingPaymentsHandler(request)
    if result_dict["result"] == "200":
        context = {
            "status":"success",
            "result_dict":result_dict
        }
    else:
        context = {
            "status":"error",
            "result_dict":result_dict
        }
    return render(request, 'everypush_payments_result.html', context)


