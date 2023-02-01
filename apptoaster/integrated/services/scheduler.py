from apscheduler.schedulers.background import BackgroundScheduler
from . import model
from . import api
from . import common
import math
import datetime

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
    model.createSystemLog(0, 'SYSTEM', 'scheduler run')

    nowDate = common.stringToDate('')
    nowTime = common.stringToTime('')
    now = common.stringToDatetime('')

    # 발송 시간이 된 푸시 확인, 스케줄에서 삭제(반복 제외), 반복 푸시일 경우 날짜 + 1
    pushList = model.readPushAll()
    workList = []
    for push in pushList:
        pushDate = push['date']
        if push['repeat']:
            pushDate = nowDate
        pushTime = push['time']
        pushDatetime = datetime.datetime.combine(pushDate, pushTime)
        if (pushDatetime - now).days < 0:
            workList.append(push)
            if push['repeat'] == True:
                model.updatePush(push['id'], push['alias'], push['title'], push['message'], push['date'] + datetime.timedelta(days=1), push['time'], push['repeat'], push['ad'])
        if push['repeat'] == False:
            model.deletePush(push['id'])

    # 푸시 발송. 푸시 기록 추가
    for push in workList:
        toaster = model.readToasterById(push['toasterId'])
        toasterTarget = model.readToasterTarget(toaster['id'])
        index = 0
        loop = math.ceil(len(toasterTarget)/100)
        for i in range(loop):
            api.kakaoSendPush(toaster['appAdminKey'], push['title'], push['message'], toasterTarget[index * 100:(index + 1)*100])
            index = index + 1
        # model.createPushHistory(toaster['id'], push['alias'], push['title'], push['message'], push['repeat'], push['ad'], len(toasterTarget))
        
    return