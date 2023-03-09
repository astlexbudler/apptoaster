from django.contrib import admin
from .models import *

class userAdmin(admin.ModelAdmin):
    list_display = ['id', 'app_name', 'email', 'tel']
    list_filter = ['id']
    search_fields = ['id']

admin.site.register(USER_TABLE, userAdmin)

class userUpdateLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'create_datetime']
    list_filter = ['id']
    search_fields = ['user_id']

admin.site.register(USER_UPDATE_LOG, userUpdateLogAdmin)

class targetAdmin(admin.ModelAdmin):
    list_display = ['token', 'user_id', 'is_push_allow', 'is_ad_allow']
    list_filter = ['token']
    search_fields = ['token', 'user_id']

admin.site.register(TARGET_TABLE, targetAdmin)

class pushAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title', 'repeat', 'ad']
    list_filter = ['id']
    search_fields = ['id', 'user_id']

admin.site.register(PUSH_SCHEDULE_TABLE, pushAdmin)

class questionAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'title', 'create_datetime']
    list_filter = ['id', 'answer', 'create_datetime']
    search_fields = ['id', 'title']

admin.site.register(QUESTION_TABLE, questionAdmin)

admin.site.register(PAYMENTS_TABLE)
admin.site.register(ADDITIONAL_USER_TABLE)
admin.site.register(LOGGER_TABLE)