from django.contrib import admin
from .models import *

admin.site.register(LOGGER_TABLE)

##################################################
# 사용자
##################################################
class userAdmin(admin.ModelAdmin):
    list_display = ['id', 'app_name', 'email', 'tel']
    list_filter = ['id']
    search_fields = ['id']

admin.site.register(USER_TABLE, userAdmin)

##################################################
# 로그인 시도
##################################################
admin.site.register(LOGIN_TRY)

##################################################
# 사용자 접속 기록
##################################################
admin.site.register(USER_ACCESS_LOG)

##################################################
# 업데이트 기록
##################################################
class userUpdateLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'create_datetime']
    list_filter = ['id']
    search_fields = ['user_id']

admin.site.register(USER_UPDATE_LOG, userUpdateLogAdmin)

##################################################
# 푸시 타겟
##################################################
class targetAdmin(admin.ModelAdmin):
    list_display = ['token', 'user_id', 'is_push_allow', 'is_ad_allow']
    list_filter = ['token']
    search_fields = ['token', 'user_id']

admin.site.register(TARGET_TABLE, targetAdmin)

##################################################
# 푸시 스케줄
##################################################
class pushAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title', 'repeat', 'ad']
    list_filter = ['id']
    search_fields = ['id', 'user_id']

admin.site.register(PUSH_SCHEDULE_TABLE, pushAdmin)

##################################################
# 질문
##################################################
class questionAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'title', 'create_datetime']
    list_filter = ['id', 'answer', 'create_datetime']
    search_fields = ['id', 'title']

admin.site.register(QUESTION_TABLE, questionAdmin)

##################################################
# 타이머
##################################################
admin.site.register(TIMER)

##################################################
# 결제정보(에브리푸시 모듈+)
##################################################
admin.site.register(PAYMENTS_TABLE)

##################################################
# 사용자부가정보(에브리푸시 모듈+)
##################################################
admin.site.register(ADDITIONAL_USER_TABLE)