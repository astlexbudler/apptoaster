from django.db import models
import datetime
##################################################
# 서버 로거
##################################################
class LOGGER_TABLE(models.Model):
    log = models.CharField(max_length=100) 
    
##################################################
# 사용자
##################################################
class USER_TABLE(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    app_icon = models.ImageField(upload_to='icon')
    app_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    tel = models.CharField(max_length=16)
    url = models.CharField(max_length=255)
    kakao_admin_key = models.CharField(max_length=255)
    create_datetime = models.DateTimeField()
    request_update = models.BooleanField()
    google_form_url = models.CharField(max_length=255)
    download_count = models.DecimalField(decimal_places=0 ,max_digits=10)
    user_count = models.DecimalField(decimal_places=0 ,max_digits=10)
    visit_today_count = models.DecimalField(decimal_places=0 ,max_digits=10)
    total_visit_count = models.DecimalField(decimal_places=0 ,max_digits=20)
    splash_background = models.ImageField(upload_to='splash_background')
    splash_logo = models.ImageField(upload_to='splash_logo')
    layout_type = models.CharField(max_length=20)
    theme = models.CharField(max_length=20)
    sales_channel = models.CharField(max_length=8, blank=True)#영업채널
##################################################
# 로그인 시도
##################################################
class LOGIN_TRY(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    count = models.DecimalField(decimal_places=0 ,max_digits=2)
##################################################
# 사용자 접속 기록
##################################################
class USER_ACCESS_LOG(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    user_id = models.CharField(max_length=10)
    ip = models.CharField(max_length=16)
    create_datetime = models.DateTimeField()
##################################################
# 업데이트 기록
##################################################
class USER_UPDATE_LOG(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    user_id = models.CharField(max_length=10)
    update_log = models.CharField(max_length=255)
    create_datetime = models.DateTimeField()
##################################################
# 푸시 타겟
##################################################
class TARGET_TABLE(models.Model):
    token = models.CharField(primary_key=True, max_length=200)
    user_id = models.CharField(max_length=20)
    uuid = models.CharField(max_length=20)
    is_push_allow = models.BooleanField()
    push_allow_datetime = models.DateTimeField(null=True, blank=True)
    is_ad_allow = models.BooleanField()
    ad_allow_datetime = models.DateTimeField(null=True, blank=True)
    last_active_datetime = models.DateTimeField()
##################################################
# 푸시 스케줄
##################################################
class PUSH_SCHEDULE_TABLE(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    user_id = models.CharField(max_length=20)
    alias = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    message = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField()
    repeat = models.BooleanField()
    ad = models.BooleanField()
##################################################
# 질문
##################################################
class QUESTION_TABLE(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    user_id = models.CharField(max_length=20)
    title = models.CharField(max_length=64)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    create_datetime = models.DateTimeField()
##################################################
# 타이머
##################################################
class TIMER(models.Model):
    index =  models.CharField(primary_key=True, max_length=32)
    datetime = models.DateTimeField()

#FOR EVERYPUSH SALES SIDE
##################################################
# 결제정보(에브리푸시 모듈+)
##################################################
class PAYMENTS_TABLE(models.Model):
    id = models.CharField(primary_key=True, max_length=20)#OrderId
    sales_channel = models.CharField(max_length=8, blank=True)
    payments_gate = models.CharField(max_length=8)
    payments_user = models.CharField(max_length=64)#From USER_TABLE, id
    payments_date = models.DateTimeField('date published', default=datetime.datetime.now)
    payments_amount = models.CharField(max_length=16)
    payments_key = models.CharField(max_length=128, blank=True)
    

##################################################
# 사용자부가정보(에브리푸시 모듈+)
##################################################
class ADDITIONAL_USER_TABLE(models.Model):
    id = models.CharField(primary_key=True, max_length=20)#From USER_TABLE, id.
    sales_channel = models.CharField(max_length=8, blank=True)#영업채널
    user_status = models.CharField(max_length=8)
    user_payday = models.DateTimeField('payments checked', default=datetime.datetime.now, blank=True)
    user_prev_payday = models.DateTimeField('last payments checked', default=datetime.datetime.now, blank=True)
    customer_key = models.CharField(max_length=128, blank=True)
    billing_key = models.CharField(max_length=128, blank=True)
    
