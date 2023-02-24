import json
import math
from . import models
from .services import api
from .services import common
from .services import email
from .services import model
from .services import session
import logging
import datetime
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

##################################################
# EVERYPUSH ORIGINAL
##################################################
########################################
# 유저 부가정보(ADDITIONAL USER DATA)
########################################
def getAdditionalUserData(request):
    try:
        try:
            userId = session.getId(request)
        except:
            req_dict = json.loads(request.body)
            userId = req_dict["userId"]
        user_additional = model.getUserAdditional(userId)
        result = {
            'status': "200",
            'user_additional': user_additional,
        }
        return(json.dumps(result))
    except:
        result = {
            'status': "500"
        }
        return(json.dumps(result))

########################################
# 일반결제 성공
########################################
def paymentsSuccessHandler(request):
    orderId = request.GET.get("orderId")
    paymentKey = request.GET.get("paymentKey")
    amount = request.GET.get("amount")
    userPrevPayday = datetime.datetime.now()
    if int(amount) <= 20000:#월플랜의 상한선은 최대 20000원임
        userStatus = "1"
        userPayday = userPrevPayday + datetime.timedelta(days=30)
    elif 20000 < int(amount) <= 200000:#연플랜의 상한선은 최대 200000원임.
        userStatus = "2"
        userPayday = userPrevPayday + datetime.timedelta(days=365)
    else:
        userStatus = "9"
    user_update_data = {#USER_TABLE을 업데이트
        "userStatus":userStatus,
        "userPayday":userPayday,#다음 결제 예정일
        "userPrevPayday":userPrevPayday,#오늘 날짜(마지막 결제일)
    }
    userId = session.getId(request)
    api_data = {#결제승인 API에 필요한 데이터
        "orderId":orderId,
        "paymentKey":paymentKey,
        "amount":amount
    }
    payments_set_data = {
        "paymentsId":orderId,
        "paymentsGate":"TOSSPG",
        "paymentsUser":userId,
        "paymentsAmount":str(amount),
        "paymentKey":paymentKey,
    }
    res_dict = api.tosspayments_approval(api_data)
    try:
        status = res_dict["status"]
        if status == "DONE":#성공적으로 결제가 승인된 경우!
            model.updateUserAdditional(user_update_data,userId)
            model.setPaymentsData(payments_set_data)
            return {"result":"200", "sys":"API Success", "api_result":res_dict, "payments_set_data":payments_set_data}
        else:
            return {"result":"500", "sys":"API Failure", "api_result":res_dict, "payments_set_data":payments_set_data}
    except:
        error_code = res_dict["code"]
        error_msg = res_dict["message"]
        return {"result":"400", "sys":"Wrong Access", "error_code":error_code, "error_msg":error_msg}

########################################
# 빌링 연동.
########################################   
def billingSuccessHandler(request):
    customerKey = request.GET.get("customerKey")
    authKey = request.GET.get("authKey")
    userId = session.getId(request)
    api_data = {
        "authKey":authKey,
        "customerKey":customerKey,
    }
    userPrevPayday = datetime.datetime.now()
    userPayday = userPrevPayday + datetime.timedelta(days=30)
    user_update_data = {
        "userStatus":"1",
        "userPayday":userPayday,#다음 결제 예정일
        "userPrevPayday":userPrevPayday,#오늘 날짜(마지막 결제일)
    }
    res_dict = api.tossbilling_approval(api_data)
    try:
        billingKey = res_dict["billingKey"]
        if ((billingKey != "") and (customerKey == res_dict["customerKey"])):#성공적으로 빌링이 연동된 경우
            user_update_data["customerKey"]=customerKey
            user_update_data["billingKey"]=billingKey
            model.updateUserAdditional(user_update_data,userId)#빌링키를 넣어준다.
            return {"result":"200", "sys":"API Success", "api_result":res_dict}
        else:
            return {"result":"500", "sys":"API Failure", "api_result":res_dict}
    except:
        error_code = res_dict["code"]
        error_msg = res_dict["message"]
        return {"result":"400", "sys":"Wrong Access", "error_code":error_code, "error_msg":error_msg}

########################################
# 빌링 결제.
########################################   
def billingPaymentsHandler(request):
    userId = session.getId(request)
    month_amount = 9900
    userPrevPayday = datetime.datetime.now()
    userPayday = userPrevPayday + datetime.timedelta(days=30)
    orderId = common.getRandomString(8)
    user_update_data = {
        "userStatus":"1",
        "userPayday":userPayday,#다음 결제 예정일
        "userPrevPayday":userPrevPayday,#오늘 날짜(마지막 결제일)
    }
    user_dict = model.getUserAdditional(userId)
    api_data = {
        "customerKey":user_dict["customer_key"],
        "billingKey":user_dict["billing_key"],
        "amount":month_amount,#월요금
        "orderId":orderId,
        "orderName":"[1개월구독]푸시알림서비스",#월플랜이름
        "taxFreeAmount":0
    }
    payments_set_data = {
        "paymentsId":orderId,
        "paymentsGate":"TOSSBL",
        "paymentsUser":userId,
        "paymentsAmount":str(month_amount),
        #"paymentsNote":paymentKey, => 이따 넣어주자
    }
    res_dict = api.tossbilling_payment_approval(api_data)#토스빌링결제요청
    try:
        status = res_dict["status"]
        if status == "DONE":#성공적으로 결제가 승인된 경우!
            model.updateUserAdditional(user_update_data,userId)
            payments_set_data["paymentKey"] = res_dict["paymentKey"]#이거 안넣으면 터짐;
            model.setPaymentsData(payments_set_data)
            return {"result":"200", "sys":"API Success", "api_result":res_dict, "payments_set_data":payments_set_data}
        else:
            return {"result":"500", "sys":"API Failure", "api_result":res_dict, "payments_set_data":payments_set_data}
    except:
        error_code = res_dict["code"]
        error_msg = res_dict["message"]
        return {"result":"400", "sys":"Wrong Access", "error_code":error_code, "error_msg":error_msg}