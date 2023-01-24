from django.contrib import admin
from .models import *

admin.site.register(SYSTEM_LOG_TABLE)
admin.site.register(LOGIN_CONTROL_TABLE)
admin.site.register(USER_TABLE)
admin.site.register(USER_EMAIL_TABLE)
admin.site.register(TARGET_TABLE)
admin.site.register(SCHEDULED_PUSH_TABLE)
admin.site.register(PUSH_HISTORY_TABLE)