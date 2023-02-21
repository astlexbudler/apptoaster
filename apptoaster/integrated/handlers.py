import json
import math
from . import models
from .services import api
from .services import common
from .services import email
from .services import model
from .services import session
import logging
logger = logging.getLogger('appToaster')


##################################################
# 앱 관리
##################################################
########################################
# 로그인
########################################
def apiLogin(request):
    ip = session.getIp(request)
    id = request.POST.get('id')

    # id를 입력하지 않음.
    if id == None:
        return {
            'status': {
                'succeed': False,
                'ip': '',
                'count': '',
            }
        }
    
    # 로그인 시도 확인
    loginTry = model.getLoginTry(ip)
    # 로그인 시도 카운트가 없을 경우 생성
    if loginTry == None:
        model.setLoginTry({"ip": ip, "count": 10})
        loginTry = {"ip": ip, "count": 10}    
    # 로그인 시도 가능 횟수 초과
    if loginTry['count'] < 1:
        return {
            'status': {
                'succeed': False,
                'ip': ip,
                'count': 0,
            }
        }
    # 로그인 시도 카운트 업데이트
    else:
        loginTry.update({
            "count": loginTry['count'] - 1
        })
        model.setLoginTry({"ip": ip, "count": loginTry['count']})

    # id 확인
    user = model.getUser(id)
    # 로그인 실패
    if user == None:
        return {
            'status': {
                'succeed': False,
                'ip': ip,
                'count': str(loginTry['count']),
            }
        }
    # 로그인 성공
    else:
        session.setId(request, user['id'])
        model.setUserAccessLog({
            'id': common.id(),
            'userId': id,
            'ip': ip,
            'createDatetime': common.stringToDatetime('')
        })
        return {
            'status': {
                'succeed': True,
                'ip': ip,
                'count': str(loginTry['count']),
            }
        }

def apiLogout(request):
    session.initSession(request)

########################################
# 대시보드
########################################
def dash(request):
    id = session.getId(request)
    user = model.getUser(id)

    return {
        'user': user,
    }

########################################
# 푸시 관리
########################################
def push(request):
    id = session.getId(request)
    user = model.getUser(id)
    pushList = []
    if user != None:
        pushList = model.getPushSchedule(user['id'])
        for push in pushList:
            push.update({
                'date': common.dateToString(push['date']),
                'time': common.timeToString(push['time']),
            })

    return {
        'user': user,
        'pushList': pushList
    }
        
########################################
# 일반 설정
########################################
def general(request):
    id = session.getId(request)
    user = model.getUser(id)
    user.update({
        "createDatetime": common.datetimeToString(user['createDatetime'])
    })

    return {
        'user': user,
    }

def generalUpdate(request):
    id = session.getId(request)
    user = model.getUser(id)

    return {
        'user': user,
    }

def apiGeneralUpdate(request):
    try:
        id = session.getId(request)
        user = models.USER_TABLE.objects.get(
            id = id
        )
        email = request.POST['email']
        tel = request.POST['tel']

        if user != None:
            model.setUser({
                "id": user.id,
                "appIcon": user.app_icon,
                "appName": user.app_name,
                "email": email,
                "tel": tel,
                "url": user.url,
                "kakaoAdminKey": user.kakao_admin_key,
                "createDatetime": user.create_datetime,
                "requestUpdate": user.request_update,
                "googleFormUrl": user.google_form_url,
                "downloadCount": user.download_count,
                "userCount": user.user_count,
                "visitTodayCount": user.visit_today_count,
                "totalVisitCount": user.total_visit_count,
                "isSplash": user.is_splash,
                "splashBackground": user.splash_background,
                "splashLogo": user.splash_logo,
                "splashMinTime": user.splash_min_time,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })
        
        return

    except:
        return

        
########################################
# 로딩 설정
########################################
def splash(request):
    id = session.getId(request)
    user = model.getUser(id)

    return {
        'user': user,
    }
        
########################################
# 레이아웃 설정
########################################
def layout(request):
    id = session.getId(request)
    user = model.getUser(id)

    return {
        'user': user,
    }
        
########################################
# 질문하기
########################################
def faq(request):
    id = session.getId(request)
    user = model.getUser(id)

    return {
        'user': user,
    }

def qna(request):
    id = session.getId(request)
    user = model.getUser(id)

    questionList = []
    if user != None:
        questionList = model.getQuestion(user['id'])
        page = request.GET.get('page', 1)
        lastPage = math.floor(len(questionList) / 100) + 1
        if page > lastPage:
            page = lastPage
        if page < 1:
            page = 1
        index = 0
        _questionList = []
        for item in questionList:
            if index >= ((page - 1) * 100) & index < ((page) * 100):
                _questionList.append(item)
            index = index + 1
        questionList = _questionList

    return {
        'user': user,
        'questionList': questionList,
    }

def apiQnaCreate(request):
    try:
        id = session.getId(request)
        user = model.getUser(id)
        title = request.POST['title']
        question = request.POST['question']

        if user != None:
            model.setQuestion({
                'id': common.id(),
                'userId': user['id'],
                'title': title,
                'question': question,
                'answer': '',
                'createDatetime': common.stringToDatetime(''),
            })

        return 

    except:
        return
        
########################################
# 접속 기록
########################################
def accessLog(request):
    id = session.getId(request)
    user = model.getUser(id)

    accessLogList = []
    if user != None:
        accessLogList = model.getUserAccessLog(user['id'])
        page = request.GET.get('page', 1)
        lastPage = math.floor(len(accessLogList) / 100) + 1
        if page > lastPage:
            page = lastPage
        if page < 1:
            page = 1
        index = 0
        _accessLogList = []
        for item in accessLogList:
            if index >= ((page - 1) * 100) & index < ((page) * 100):
                _accessLogList.append(item)
            index = index + 1
        accessLogList = _accessLogList
        for accessLog in accessLogList:
            accessLog.update({
                'createDatetime': common.datetimeToString(accessLog['createDatetime'])
            })

    return {
        'user': user,
        'accessLogList': accessLogList,
    }
    
        
########################################
# 업데이트 기록
########################################
def updateLog(request):
    id = session.getId(request)
    user = model.getUser(id)

    updateLogList = []
    if user != None:
        updateLogList = model.getUserUpdateLog(id)
        page = request.GET.get('page', 1)
        lastPage = math.floor(len(updateLogList) / 100) + 1
        if page > lastPage:
            page = lastPage
        if page < 1:
            page = 1
        index = 0
        _updateLogList = []
        for item in updateLogList:
            if index >= ((page - 1) * 100) & index < ((page) * 100):
                _updateLogList.append(item)
            index = index + 1
        updateLogList = _updateLogList
        for i in updateLogList:
            i.update({
                'createDatetime': common.datetimeToString(i['createDatetime'])
            })

    return {
        'user': user,
        'updateLogList': updateLogList,
    }



##################################################
# 앱 토스터 API
##################################################
########################################
# 수신인 관리(GET/POST)
########################################
def apiGetTarget(request, id):
    try:
        user = models.USER_TABLE.objects.get(
            id = id
        )
        token = request.GET['token']
        target = model.getTarget(token)

        # 없을경우 생성, 다운로드 및 방문자 수, 사용자 수 증가
        if target == None:
            model.setTarget({
                "token": token,
                "userId": user.id,
                "uuid": common.uuid(),
                "isPushAllow": False,
                "pushAllowDatetime": common.stringToDatetime(''),
                "isAdAllow": False,
                "adAllowDatetime": common.stringToDatetime(''),
                "lastActiveDate": common.stringToDate(''),
            })
            model.setUser({
                "id": user.id,
                "appIcon": user.app_icon,
                "appName": user.app_name,
                "email": user.email,
                "tel": user.tel,
                "url": user.url,
                "kakaoAdminKey": user.kakao_admin_key,
                "createDatetime": user.create_datetime,
                "requestUpdate": user.request_update,
                "googleFormUrl": user.google_form_url,
                "downloadCount": user.download_count + 1,
                "userCount": user.user_count + 1,
                "visitTodayCount": user.visit_today_count + 1,
                "totalVisitCount": user.total_visit_count + 1,
                "isSplash": user.is_splash,
                "splashBackground": user.splash_background,
                "splashLogo": user.splash_logo,
                "splashMinTime": user.splash_min_time,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })
            target = model.getTarget(token)
            return json.dumps({
                'status': 'new',
                'target': target
            })

        # 사용자가 오늘 처음 방문했다면 방문자 수 증가
        if int((common.stringToDate('') - target['lastActiveDate']).days) > 0:
            model.setTarget({
                "token": target['token'],
                "userId": target['userId'],
                "uuid": target['uuid'],
                "isPushAllow": target['isPushAllow'],
                "pushAllowDatetime": target['pushAllowDatetime'],
                "isAdAllow": target['isAdAllow'],
                "adAllowDatetime": target['adAllowDatetime'],
                "lastActiveDate": common.stringToDate(''),
            })
            model.setUser({
                "id": user.id,
                "appIcon": user.app_icon,
                "appName": user.app_name,
                "email": user.email,
                "tel": user.tel,
                "url": user.url,
                "kakaoAdminKey": user.kakao_admin_key,
                "createDatetime": user.create_datetime,
                "requestUpdate": user.request_update,
                "googleFormUrl": user.google_form_url,
                "downloadCount": user.download_count,
                "userCount": user.user_count,
                "visitTodayCount": user.visit_today_count + 1,
                "totalVisitCount": user.total_visit_count + 1,
                "isSplash": user.is_splash,
                "splashBackground": user.splash_background,
                "splashLogo": user.splash_logo,
                "splashMinTime": user.splash_min_time,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })

        return json.dumps({
            'status': 'exist',
            'target': target
        })
    except:
        return json.dumps({
            'status': 'error'
        })

def apiPatchTarget(request, id):
    try:
        user = model.getUser(id)
        token = request.GET['token']
        isPushAllow = request.GET['isPushAllow']
        target = model.getTarget(token)
        if isPushAllow == 'true':
            api.kakaoRegisterTarget(user['appAdminKey'], target['uuid'], target['token'])
            isPushAllow = True
        else:
            isPushAllow = False
            api.kakaoDeleteTarget(user['appAdminKey'], target['uuid'])
        isAdAllow = request.GET['isAdAllow']
        if isAdAllow == 'true':
            isAdAllow = True
        else:
            isAdAllow = False
        model.setTarget({
            "token": target['token'],
            "userId": target['userId'],
            "uuid": target['uuid'],
            "isPushAllow": isPushAllow,
            "pushAllowDatetime": common.stringToDatetime(''),
            "isAdAllow": isAdAllow,
            "adAllowDatetime": common.stringToDatetime(''),
            "lastActiveDate": target['lastActiveDate'],
        })

        return
    except:
        return

##################################################
# 푸시
##################################################
########################################
# 푸시 관리(POST/DELETE)
########################################
def apiPostPush(request, user):
    try:
        id = request.POST.get('id', common.id())
        alias = request.POST['alias']
        title = request.POST['title']
        message = request.POST['message']
        date = common.stringToDate(request.POST.get('date', ''))
        time = common.stringToTime(request.POST.get('time', '') + ':00')
        repeat = request.POST['repeat']
        if repeat == '2':
            repeat = True
        else:
            repeat = False
        if request.POST.get('ad', '') == 'on':
            ad = True
        else:
            ad = False

        model.setPushSchedule({
            "id": id,
            "userId": user['id'],
            "alias": alias,
            "title": title,
            "message": message,
            "date": date,
            "time": time,
            "repeat": repeat,
            "ad": ad,
        })

        return 'toast_push_success.html'
    except:
        return 'toast_push_fail.html'

def apiDeletePush(request, user):
    try:
        id = request.GET['id']
        model.deletePushSchedule(id)

        return 'toast_push_success.html'
    except:
        return 'toast_push_fail.html'