
from apscheduler.schedulers.background import BackgroundScheduler
from . import model
from . import api
from . import common
from . import email
from .. import models
import math
import datetime
import logging
logger = logging.getLogger('appToaster')

'''
scheduler.py
스케줄러 관련 기능을 관리하는 서비스입니다.

스케줄러가 해야할 일 목록
1. 푸시 스케줄 확인 후 시간이 지난 푸시 목록 확보
2. 위 푸시 송신
3. 푸시 기록 테이블로 이동, 원본 삭제
'''

##################################################
# 스케줄러
##################################################
def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', seconds=100)
    scheduler.start()

def scheduled_job():
    nowDate = common.stringToDate('')
    nowTime = common.stringToTime('')
    nowDatetime = common.stringToDatetime('')
    logger.info('스케줄러 실행')

    # 하루 마감
    try:
        # 이전 마간 날짜 확인
        clearDatetime = models.TIMER.objects.get(
            index = 'clearDatetime'
        )
        clearDatetime = clearDatetime.datetime
        logger.info("어제자 마감 날짜: " + clearDatetime)
    except:
        models.TIMER(
            index = 'clearDatetime',
            datetime = nowDatetime
        ).save()
        clearDatetime = nowDatetime

    # 마감 날짜로부터 만 1일 경과 시
    if int((clearDatetime - nowDatetime).days) < -1:
        logger.info("마감 날짜로부터 1일 이상 경과 확인")
        models.TIMER(
            index = 'clearDatetime',
            datetime = nowDatetime
        ).save()

    # 미답변 질문 확인
        not_answered = models.QUESTION_TABLE.objects.all().filter(
            answer=""
        )
        if len(not_answered) > 0:
            logger.info('미답변 질문 발견 ' + str(len(not_answered)) + "개의 미답변 질문이 발견되었습니다.")
            email.sendEmail("toast@apptoaster.co.kr", "미답변 Qna 질문이 있습니다.", '미답변 질문 발견 ' + str(len(not_answered)) + "개의 미답변 질문이 발견되었습니다.")
        
        # 100일 이상 접속하지 않은 사용자 제거
        targetList = models.TARGET_TABLE.objects.all()
        for target in targetList:
            if int((target.last_active_datetime - nowDatetime).days) < -100:
                logger.info("100일 이상 접속하지 않은 사용자 확인. " + target.pk[0:10] + "...")
                models.TARGET_TABLE.objects.get(
                    token = target.token
                ).delete()

        # 일일 방문자 횟수 초기화, 사용자 수 다시 계산
        userList = models.USER_TABLE.objects.all()
        for user in userList:
            logger.info("앱 " + user.app_name + "방문자 초기화")
            targetLen = len(models.TARGET_TABLE.objects.all().filter(
                user_id = user.id
            ))
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
                "userCount": targetLen,
                "visitTodayCount": 0,
                "totalVisitCount": user.total_visit_count,
                "splashBackground": user.splash_background,
                "splashLogo": user.splash_logo,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })

    # 로그인 카운트 초기화
    logger.info("로그인 차단 초기화")
    model.initLoginTry()

    # 발송 시간이 된 푸시 확인, 스케줄에서 삭제(반복 제외), 반복 푸시일 경우 날짜 + 1
    pushList = model.getPushScheduleAll()
    workList = []
    for push in pushList:
        pushDate = push['date']
        pushTime = push['time']
        pushDatetime = datetime.datetime.combine(pushDate, pushTime)
        if int((pushDatetime - nowDatetime).days) < 0:
            logger.info(push["title"] + " 푸시 발송")
            workList.append(push)
            if push['repeat']:
                logger.info(push["title"] + " 내일 반복 설정")
                model.setPushSchedule({
                    "id": push['id'],
                    "userId": push['userId'],
                    "alias": push['alias'],
                    "title": push['title'],
                    "message": push['message'],
                    "date": push['date'] + datetime.timedelta(days=1),
                    "time": push['time'],
                    "repeat": push['repeat'],
                    "ad": push['ad'],
                })
            else:
                logger.info(push["title"] + " 푸시 삭제")
                model.deletePushSchedule(push['id'])

    # 푸시 발송. 푸시 기록 추가
    for push in workList:
        user = model.getUser(push['userId'])
        targetList = model.getTargetAll(push['userId'])
        index = 0
        loop = math.ceil(len(targetList)/100)

        list = []
        for target in targetList:
            if target['isPushAllow']:
                list.append(target)
        targetList = list

        if push['ad']:
            push['message'] = '(광고)' + push['message'] + '\n(수신거부:앱 메뉴 알림 설정)'
            list = []
            for target in targetList:
                if target['isAdAllow']:
                    list.append(target)
            targetList = list

        for i in range(loop):
            api.kakaoSendPush(user['kakaoAdminKey'], push['title'], push['message'], targetList[index * 100:(index + 1)*100 - 1])
            index = index + 1