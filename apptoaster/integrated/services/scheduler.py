from apscheduler.schedulers.background import BackgroundScheduler

##################################################
# 스케줄러
##################################################
def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', seconds=180)
    scheduler.start()

def scheduled_job():
    return