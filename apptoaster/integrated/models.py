from django.db import models

##################################################
# 시스템 기록 테이블
##################################################
class SYSTEM_LOG_TABLE(models.Model):
    # 식별자
    id = models.CharField(primary_key=True, max_length=20)
    # 위험도
    # 0에서 9로 갈수록 위험한 메세지
    level = models.DecimalField(decimal_places=0 ,max_digits=1)
    # 등록된 어플리케이션 이름 
    application_name = models.CharField(max_length=64)
    # 메세지
    message = models.CharField(max_length=255)



##################################################
# 로그인 관리 테이블
##################################################
class LOGIN_CONTROL_TABLE(models.Model):
    # ip(식별자)
    ip = models.CharField(primary_key=True, max_length=64)
    # 로그인 시도 가능 횟수/최대 4 -> 0
    count = models.DecimalField(decimal_places=0 ,max_digits=1)



##################################################
# 앱 토스터 고객 테이블
##################################################
class TOASTER_TABLE(models.Model):
    # 식별자
    id = models.CharField(primary_key=True, max_length=20)
    # API/로그인용 인증키
    key = models.CharField(max_length=64)
    # 등록된 어플리케이션 아이콘
    application_icon = models.ImageField(upload_to='icons')
    # 등록된 어플리케이션 이름
    application_name = models.CharField(max_length=64)
    # 이메일
    email = models.CharField(max_length=64)
    # 전화번호
    tel = models.CharField(max_length=64)
    # 카카오 키
    app_admin_key = models.CharField(max_length=255)
    # 생성일
    create_date = models.DateField()
    # 만료일
    expire_date = models.DateField()
    # 푸시 서비스
    is_push = models.BooleanField()
    


##################################################
# 앱 사용자 테이블
##################################################
class TARGET_TABLE(models.Model):
    # 식볗자
    id = models.CharField(primary_key=True, max_length=20)
    # 토큰
    token = models.CharField(max_length=255)
    # 앱 토스터 고객 식별자
    toaster_id = models.CharField(max_length=20)
    # 기기 타입/gcm, apns
    device_type = models.CharField(max_length=8)
    # 푸시 허용
    is_push_allow = models.BooleanField()
    # 푸시 허용 동의 시간
    push_allow_datetime = models.DateTimeField(null=True, blank=True)
    # 광고 허용
    is_ad_allow = models.BooleanField()
    # 광고 허용 동의 시간
    ad_allow_datetime = models.DateTimeField(null=True, blank=True)
    # 마지막 활동 날짜
    last_active_date = models.DateField()



##################################################
# PUSH 예약 테이블
##################################################
class SCHEDULED_PUSH_TABLE(models.Model):
    # 식별자
    id = models.CharField(primary_key=True, max_length=20)
    # 앱 토스터 고객 식별자
    toaster_id = models.CharField(max_length=20)
    # 푸시 이름
    alias = models.CharField(max_length=64)
    # 푸시 제목
    title = models.CharField(max_length=64)
    # 푸시 메세지
    message = models.CharField(max_length=255)
    # 발송 날짜
    date = models.DateField(null=True, blank=True)
    # 발송 시간
    time = models.TimeField()
    # 반복 여부
    repeat = models.BooleanField()
    # 광고 여부
    ad = models.BooleanField()
    # 직접 대상 지정 여부
    is_assigned = models.BooleanField()

class ASSIGNED_TARGET(models.Model):
    # 푸시 식별자
    push_id = models.CharField(max_length=20)
    # 타겟 식별자
    target_id = models.CharField(max_length=20)




##################################################
# PUSH 기록
##################################################
class PUSH_HISTORY_TABLE(models.Model):
    # 앱 토스터 고객 식별자
    toaster_id = models.CharField(max_length=20)
    # 푸시 이름
    alias = models.CharField(max_length=64)
    # 푸시 제목
    title = models.CharField(max_length=64)
    # 푸시 메세지
    message = models.CharField(max_length=255)
    # 발송 시간
    toasted_datetime = models.DateTimeField()
    # 반복 여부
    repeat = models.BooleanField()
    # 광고 여부
    ad = models.BooleanField()
    # 수신 카운트
    count = models.DecimalField(decimal_places=0 ,max_digits=10)