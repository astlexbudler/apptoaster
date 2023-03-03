
from apscheduler.schedulers.background import BackgroundScheduler
from . import model
from . import api
from . import common
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
    scheduler.add_job(scheduled_job, 'interval', seconds=60)
    scheduler.start()

def scheduled_job():
    nowDate = common.stringToDate('')
    nowTime = common.stringToTime('')
    nowDatetime = common.stringToDatetime('')
    logger.info('스케줄러 실행')

    # 하루 마감
    try:
        clearDatetime = models.TIMER.objects.get(
            index = 'clearDatetime'
        )
        clearDatetime = clearDatetime.datetime
    except:
        models.TIMER(
            index = 'clearDatetime',
            datetime = nowDatetime
        ).save()
        clearDatetime = nowDatetime
    if int((clearDatetime - nowDatetime).days) < -1:
        models.TIMER(
            index = 'clearDatetime',
            datetime = nowDatetime
        ).save()
        # 100일 이상 접속하지 않은 사용자 제거
        targetList = models.TARGET_TABLE.objects.all()
        for target in targetList:
            if int((target.last_active_datetime - nowDatetime).days) < -100:
                models.TARGET_TABLE.objects.get(
                    token = target.token
                ).delete()

        # 일일 방문자 횟수 초기화, 사용자 수 다시 계산
        userList = models.USER_TABLE.objects.all()
        for user in userList:
            targetLen = len(models.TARGET_TABLE.objects.all().filter(
                user_id = user['id']
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
                "isSplash": user.is_splash,
                "splashBackground": user.splash_background,
                "splashLogo": user.splash_logo,
                "splashMinTime": user.splash_min_time,
                "layoutType": user.layout_type,
                "theme": user.theme,
            })

    # 로그인 카운트 초기화
    model.initLoginTry()

    # 발송 시간이 된 푸시 확인, 스케줄에서 삭제(반복 제외), 반복 푸시일 경우 날짜 + 1
    pushList = model.getPushScheduleAll()
    workList = []
    for push in pushList:
        pushDate = push['date']
        pushTime = push['time']
        pushDatetime = datetime.datetime.combine(pushDate, pushTime)
        if int((pushDatetime - nowDatetime).days) < 0:
            workList.append(push)
            if push['repeat']:
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
            api.kakaoSendPush(user['appAdminKey'], push['title'], push['message'], targetList[index * 100:(index + 1)*100 - 1])
            index = index + 1