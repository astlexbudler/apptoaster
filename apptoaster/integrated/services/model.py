from ..models import *
from . import common
import logging
import datetime
logger = logging.getLogger('appToaster')

'''
model.py
데이터베이스 관련 기능을 관리하는 서비스입니다.
'''
##################################################
# 사용자
##################################################
########################################
# 사용자 set
########################################
def setUser(user):
    USER_TABLE(
        id = user['id'],
        app_icon = user['appIcon'],
        app_name = user['appName'],
        email = user['email'],
        tel = user['tel'],
        url = user['url'],
        kakao_admin_key = user['kakaoAdminKey'],
        create_datetime = user['createDatetime'],
        request_update = user['requestUpdate'],
        google_form_url = user['googleFormUrl'],
        download_count = user['downloadCount'],
        user_count = user['userCount'],
        visit_today_count = user['visitTodayCount'],
        total_visit_count = user['totalVisitCount'],
        is_splash = user['isSplash'],
        splash_background = user['splashBackground'],
        splash_logo = user['splashLogo'],
        splash_min_time = user['splashMinTime'],
        layout_type = user['layoutType'],
        theme = user['theme'],
    ).save()

########################################
# 사용자 get
########################################
def getUser(id):
    try:
        user = USER_TABLE.objects.get(
            id = id
        )

        return {
            "id": user.id,
            "appIcon": 'media/' + str(user.app_icon),
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
            "visitTodayCount": user.visit_today_count,
            "totalVisitCount": user.total_visit_count,
            "isSplash": user.is_splash,
            "splashBackground": 'media/' + str(user.splash_background),
            "splashLogo": 'media/' + str(user.splash_logo),
            "splashMinTime": user.splash_min_time,
            "layoutType": user.layout_type,
            "theme": user.theme,
        }

    except Exception as e:
        logger.info(e)
        return

########################################
# 사용자 get all
########################################
def getUserAll():
    try:
        list = USER_TABLE.objects.all()

        userList = []
        for user in list:
            userList.append({
                "id": user.id,
                "appIcon": 'media/' + str(user.app_icon),
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
                "visitTodayCount": user.visit_today_count,
                "totalVisitCount": user.total_visit_count,
                "isSplash": user.is_splash,
                "splashBackground": 'media/' + str(user.splash_background),
                "splashLogo": 'media/' + str(user.splash_logo),
                "splashMinTime": user.splash_min_time,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })

        return userList

    except Exception as e:
        logger.info(e)
        return

########################################
# 사용자 delete
########################################
def deleteUser(userId):
    try:
        USER_TABLE.objects.get(
            id = userId
        ).delete()

    except:
        return



##################################################
# 로그인 시도
##################################################
########################################
# 로그인 시도 set
########################################
def setLoginTry(loginTry):
    LOGIN_TRY(
        ip = loginTry['ip'],
        count = loginTry['count']
    ).save()

########################################
# 로그인 시도 get
########################################
def getLoginTry(ip):
    try:
        loginTry = LOGIN_TRY.objects.get(
            ip = ip
        )

        return {
            'ip': loginTry.ip,
            'count': loginTry.count
        }
    except:
        return

########################################
# 로그인 시도 초기화
########################################
def initLoginTry():
    LOGIN_TRY.objects.all().delete()



##################################################
# 사용자 접속 기록
##################################################
########################################
# 사용자 접속 기록 set
########################################
def setUserAccessLog(userAccessLog):
    USER_ACCESS_LOG(
        id = userAccessLog['id'],
        user_id = userAccessLog['userId'],
        ip = userAccessLog['ip'],
        create_datetime = userAccessLog['createDatetime'],
    ).save()

########################################
# 사용자 접속 기록 get
########################################
def getUserAccessLog(userId):
    try:
        list = USER_ACCESS_LOG.objects.all().filter(
            user_id = userId
        )

        userAccessLogList = []
        for item in list:
            userAccessLogList.append({
                "id": item.id,
                "userId": item.user_id,
                "ip": item.ip,
                "createDatetime": item.create_datetime,
            })

        return userAccessLogList
    
    except:
        return []

########################################
# 사용자 접속 기록 delete
########################################
def deleteUserAccessLog(id):
    try:
        USER_ACCESS_LOG.objects.get(
            id = id
        ).delete()

    except:
        return

########################################
# 사용자 접속 기록 init
########################################
def initUserAccessLog(userId):
    try:
        USER_ACCESS_LOG.objects.all().filter(
            user_id = userId
        ).delete()

    except:
        return



##################################################
# 업데이트 기록
##################################################
########################################
# 업데이트 기록 set
########################################
def setUserUpdateLog(userUpdateLog):
    USER_UPDATE_LOG(
        id = userUpdateLog['id'],
        user_id = userUpdateLog['userId'],
        update_log = userUpdateLog['updateLog'],
        create_datetime = userUpdateLog['createDatetime'],
    ).save()

########################################
# 업데이트 기록 get
########################################
def getUserUpdateLog(id):
    try:
        list = USER_UPDATE_LOG.objects.all().filter(
            user_id = id
        )

        userUpdateLogList = []
        for item in list:
            userUpdateLogList.append({
                "id": item.id,
                "userId": item.user_id,
                "updateLog": item.update_log,
                "createDatetime": item.create_datetime,
            })

        return userUpdateLogList
    
    except:
        return []

########################################
# 업데이트 기록 init
########################################
def initUserUpdateLog(userId):
    try:
        USER_UPDATE_LOG.objects.all().filter(
            user_id = userId
        ).delete()

    except:
        return



##################################################
# 푸시 타겟
##################################################
########################################
# 푸시 타겟 set
########################################
def setTarget(target):
    TARGET_TABLE(
        token = target["token"],
        user_id = target["userId"],
        uuid = target["uuid"],
        is_push_allow = target["isPushAllow"],
        push_allow_datetime = target["pushAllowDate"],
        is_ad_allow = target["isAdAllow"],
        ad_allow_datetime = target["adAllowDatetime"],
        last_active_datetime = target["lastActiveDatetime"],
    ).save()

########################################
# 푸시 타겟 get
########################################
def getTarget(token):
    try:
        target = TARGET_TABLE.objects.get(
            token = token
        )

        return {
            "token": target.token,
            "userId": target.user_id,
            "uuid": target.uuid,
            "isPushAllow": target.is_push_allow,
            "pushAllowDate": target.push_allow_datetime,
            "isAdAllow": target.is_ad_allow,
            "adAllowDatetime": target.ad_allow_datetime,
            "lastActiveDatetime": target.last_active_datetime,
        }
    except:
        return

########################################
# 푸시 타겟 get all
########################################
def getTargetAll(userId):
    try:
        list = TARGET_TABLE.objects.all().filter(
            user_id = userId
        )

        targetList = []
        for item in list:
            targetList.append({
                "token": item.token,
                "userId": item.user_id,
                "uuid": item.uuid,
                "isPushAllow": item.is_push_allow,
                "pushAllowDate": item.push_allow_datetime,
                "isAdAllow": item.is_ad_allow,
                "adAllowDatetime": item.ad_allow_datetime,
                "lastActiveDatetime": item.last_active_datetime,
            })

        return targetList
    
    except:
        return []

########################################
# 푸시 타겟 delete
########################################
def deleteTarget(token):
    try:
        TARGET_TABLE.objects.get(
            token = token
        ).delete()

    except:
        return

########################################
# 푸시 타겟 init
########################################
def deleteTarget(userId):
    try:
        TARGET_TABLE.objects.all().filter(
            user_id = userId,
        ).delete()

    except:
        return



##################################################
# 푸시 스케줄
##################################################
########################################
# 푸시 스케줄 set
########################################
def setPushSchedule(pushSchedule):
    PUSH_SCHEDULE_TABLE(
        id = pushSchedule['id'],
        user_id = pushSchedule['userId'],
        alias = pushSchedule['alias'],
        title = pushSchedule['title'],
        message = pushSchedule['message'],
        date = pushSchedule['date'],
        time = pushSchedule['time'],
        repeat = pushSchedule['repeat'],
        ad = pushSchedule['ad'],
    ).save()

########################################
# 푸시 스케줄 get all
########################################
def getPushScheduleAll():
    try:
        list = PUSH_SCHEDULE_TABLE.objects.all()
        
        pushScheduleList = []
        for item in list:
            pushScheduleList.append({
                "id": item.id,
                "userId": item.user_id,
                "alias": item.alias,
                "title": item.title,
                "message": item.message,
                "date": item.date,
                "time": item.time,
                "repeat": item.repeat,
                "ad": item.ad,
            })
        
        return pushScheduleList

    except:
        return []

########################################
# 푸시 스케줄 get
########################################
def getPushSchedule(userId):
    try:
        list = PUSH_SCHEDULE_TABLE.objects.all().filter(
            user_id = userId
        )
        
        pushScheduleList = []
        for item in list:
            pushScheduleList.append({
                "id": item.id,
                "userId": item.user_id,
                "alias": item.alias,
                "title": item.title,
                "message": item.message,
                "date": item.date,
                "time": item.time,
                "repeat": item.repeat,
                "ad": item.ad,
            })
        
        return pushScheduleList

    except:
        return []

########################################
# 푸시 스케줄 delete
########################################
def deletePushSchedule(id):
    try:
        PUSH_SCHEDULE_TABLE.objects.get(
            id = id
        ).delete()

    except:
        return

########################################
# 푸시 스케줄 init
########################################
def initPushSchedule(userId):
    try:
        PUSH_SCHEDULE_TABLE.objects.all().filter(
            user_id = userId,
        ).delete()

    except:
        return



##################################################
# 질문
##################################################
########################################
# 질문 set
########################################
def setQuestion(question):
    QUESTION_TABLE(
        id = question['id'],
        user_id = question['userId'],
        title = question['title'],
        question = question['question'],
        answer = question['answer'],
        create_datetime = question['createDatetime'],
    ).save()

########################################
# 질문 get all(미답변)
########################################
def getQuestionAll():
    try:
        list = QUESTION_TABLE.objects.all().filter(
            answer = ''
        )
        
        questionList = []
        for item in list:
            questionList.append({
                "id": item.id,
                "userId": item.user_id,
                "title": item.title,
                "question": item.question,
                "answer": item.answer,
                "createDatetime": item.create_datetime,
            })
        
        return questionList

    except:
        return []

########################################
# 질문 get
########################################
def getQuestion(userId):
    try:
        list = QUESTION_TABLE.objects.all().filter(
            user_id = userId
        )
        
        questionList = []
        for item in list:
            questionList.append({
                "id": item.id,
                "userId": item.user_id,
                "title": item.title,
                "question": item.question,
                "answer": item.answer,
                "createDatetime": common.datetimeToString(item.create_datetime),
            })
        
        return questionList

    except:
        return []

########################################
# 질문 init
########################################
def initQuestion(userId):
    try:
        QUESTION_TABLE.objects.all().filter(
            user_id = userId,
        ).delete()

    except:
        return
########################################
# 유저 부가정보(ADDITIONAL USER DATA)
########################################
def getUserAdditional(userId):
    try:
        table = ADDITIONAL_USER_TABLE.objects.get(
            id = userId
        )
        result = {
            "id": table.id,
            "sales_channel": table.sales_channel,
            "user_status": table.user_status,
            "user_payday": common.datetimeToString(table.user_payday),
            "user_prev_payday": common.datetimeToString(table.user_prev_payday),
            "customer_key": table.customer_key,
            "billing_key": table.billing_key,
            "left_time": (table.user_payday - datetime.datetime.now()).days,
        }
        if ((result['left_time'] < -1) and (table.user_status == "1")):#빌링이 필요한경우 :즉, 서비스 만료 상태이면서 
            table.user_status = "B"#알파벳 'B'는 '빌링이 필요한 상태'를 의미함.
            table.save()
            result["user_status"] = "B"
        else:
            pass
        return result
    except Exception as e:
        logger.info(e)
        return

########################################
# 유저 부가정보 UPDATE&SET
########################################
def updateUserAdditional(update_dict,userId):
    try:
        table = ADDITIONAL_USER_TABLE.objects.get(id=userId)
    except:
        ADDITIONAL_USER_TABLE(
            id = userId,
            sales_channel = "EVRP",
            user_status = "0",
        ).save()
        table = ADDITIONAL_USER_TABLE.objects.get(id=userId)
    for key in update_dict:
        if key == "salesChannel":
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.sales_channel = update_dict[key]
        elif key == "userStatus":
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.user_status = update_dict[key]
        elif key == "userPayday":#자료형 변경에 주의
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.user_payday= update_dict[key]
        elif key == "userPrevPayday":#자료형 변경에 주의
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.user_prev_payday= update_dict[key]
        elif key == "customerKey":
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.customer_key = update_dict[key]
        elif key == "billingKey":
            if update_dict[key] == "":#blank값인 경우, 업데이트 무시.
                continue
            else:
                pass
            table.billing_key = update_dict[key]
    table.save()
    return True

########################################
# 결제정보 set
########################################
def setPaymentsData(update_dict):
    PAYMENTS_TABLE(
        id = update_dict['paymentsId'],#orderId
        sales_channel = "EVRP",
        payments_gate = update_dict['paymentsGate'],
        payments_user = update_dict['paymentsUser'],
        payments_date = datetime.datetime.now(),
        payments_amount = update_dict['paymentsAmount'],
        payments_key = update_dict["paymentKey"],#여긴 s없음.(주의!)
    ).save()
    return True