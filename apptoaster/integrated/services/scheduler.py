from apscheduler.schedulers.background import BackgroundScheduler

'''
scheduler.py
스케줄러 관련 기능을 관리하는 서비스입니다.

스케줄러가 해야할 일 목록
1. 이메일 수신함 확인 후 이메일 명령 처리
2. 푸시 스케줄 테이블 확인 후 푸시 발송 처리
'''

##################################################
# 스케줄러
##################################################
def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', seconds=180)
    scheduler.start()

def scheduled_job():

    return