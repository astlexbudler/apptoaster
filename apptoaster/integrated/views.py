from django.shortcuts import render
from django.http import HttpResponse
from .handlers import *
from django.views.decorators.csrf import csrf_exempt
from .models import *
import logging
import datetime
from .services import email

logger = logging.getLogger('appToaster')

##################################################
# 웹 페이지 경로
##################################################
# 메인 페이지
def webIndex(request):
    return render(request, "index.html")

# 서비스 이용 약관
def webPolicy(request):
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
    email.sendEmail('astlexbudler@naver.com', '앱 토스터 관리자 이메일', 
    '''
    <form method="POST" action="https://apptoaster.co.kr/api/toast_push/key/00000000" target="_blank">
        <table style="
width: 650px;
margin: auto;
padding: 25px 75px 25px 75px;
color: rgb(50, 50, 50);
font-size: 16px;
font-weight: 300;
word-break: break-all;">
            <thead>
                <tr>
                    <td>
                        <img src="http://127.0.0.1:8000/static/default/img/logos/APPTOASTER.png" style="
width: 250px;">
                    </td>
                    <td colspan="3" style="
text-align: end;">
                        <span style="background-color: rgb(75, 75, 75); color: white;">
                            PUSH 보내기
                        </span>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="
padding: 15px 0px 15px 0px;">
                        <hr style="
border: 0;
border-top: 1px solid gainsboro;">
                    </td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="4" style="font-size: 12px; padding-bottom: 15px;">
                        push to. 앱 토스터 - 가장 쉽고 빠른 앱 출시!
                    </td>
                </tr>
                <tr>
                    <td colspan="4">
                        <div style="display: inline-block;">
                            <label style="display: block;">이름(최대 24자)</label>
                            <input value="제목 없음" maxlength="24"
                                style="width: 215px; border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px;">
                        </div>
                        <div style="display: inline-block;">
                            <label style="display: block;">푸시 제목(최대 32자) <span style="color: red;">*</span></label>
                            <input value="앱 토스터! - 가장 쉽고 빠른 앱 출시!" maxlength="32"
                                style="width: 215px; border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; margin-left: 4px;">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="padding-top: 5px;">
                        <div style="display: inline-block;">
                            <label style="display: block;">푸시 내용(최대 255자) <span style="color: red;">*</span></label>
                            <textarea placeholder="메세지를 입력해주세요." maxlength="255"
                                style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 471px;"
                                required></textarea>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-top: 5px;" colspan="4">
                        <div style="display: inline-block;">
                            <label style="display: block;">예약 선택 <span style="color: red;">*</span></label>
                            <select
                                style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 202px; margin-right: 4px;">
                                <option selected>
                                    예약 안함
                                </option>
                                <option>
                                    예약하고 한번
                                </option>
                                <option>
                                    매일 반복
                                </option>
                            </select>
                        </div>
                        <div style="display: inline-block;">
                            <label style="display: block;">예약 날짜</label>
                            <input type="date"
                                style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 110px; margin-right: 4px;">
                        </div>
                        <div style="display: inline-block;">
                            <label style="display: block;">예약 시간</label>
                            <input type="time"
                                style="border-radius: 0px; border: 1px solid gainsboro; padding: 10px 15px 10px 15px; width: 110px;">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="font-size: 12px; color: gray;">
                        * 예약 안함 선택 시 <span style="text-decoration: underline;">예약 날짜</span> 및 <span
                            style="text-decoration: underline;">예약 시간</span>을 입력하지 않으셔도 됩니다.<br>
                        * 매일 반복 선택 시 <span style="text-decoration: underline;">예약 날짜</span>을 입력하지 않으셔도 됩니다.
                    </td>
                </tr>
                <tr>
                    <td style="padding-top: 5px;" colspan="4">
                        <input type="checkbox">
                        <label>광고성 푸시 메세지 여부 <small>(광고성 푸시 메세지일 경우 체크박스 클릭)</small></label>
                    </td>
                </tr>
                <tr>
                    <td colspan="4">
                        <input type="checkbox" required>
                        <label>개인정보 처리 방침 및 이용약관 동의 <span style="color: red;">*</span></label>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="padding-top: 50px;">
                        <button
                            style="border-radius: 0px; background-color: rgb(75, 75, 75); border: 0; color: white; padding: 10px 15px 10px 15px; width: 503px;">
                            보내기
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
    <table style="
width: 650px;
margin: auto;
padding: 25px 75px 25px 75px;
color: rgb(50, 50, 50);
font-size: 16px;
font-weight: 300;
background-color: gainsboro;">
        <tr>
            <td colspan="2">
                <img src="http://127.0.0.1:8000/static/default/img/logos/APPTOASTER.png" style="
width: 200px;">
            </td>
            <td colspan="2" style="font-size: 12px; padding-left: 50px;">
                <a href="#" style="color: rgb(50, 50, 50);">개인정보 처리방침 및 이용약관 ></a><br>
                <a href="#" style="color: rgb(50, 50, 50);">한국 인터넷 진흥원 푸시 메세지 안내 확인 ></a>
            </td>
        </tr>
        <tr>
            <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
                <a href="#" style="color: rgb(50, 50, 50);">계정 관리</a>
                <span> / </span>
                <a href="#" style="color: rgb(50, 50, 50);">푸시 삭제/수정</a>
                <span> / </span>
                <a href="#" style="color: rgb(50, 50, 50);">푸시 기록 확인</a>
            </td>
        </tr>
        <tr>
            <td colspan="4" style="text-align: center; font-size: 12px; padding-top: 50px;">
                © 2023 AppToaster. All Rights Reserved.
            </td>
        </tr>
    </table>
    ''')
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