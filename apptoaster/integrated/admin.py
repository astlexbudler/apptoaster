from django.contrib import admin
from .models import *

admin.site.register(SYSTEM_LOG_TABLE)
admin.site.register(LOGIN_CONTROL_TABLE)
admin.site.register(TOASTER_TABLE)
admin.site.register(TARGET_TABLE)
admin.site.register(ASSIGNED_TARGET_TABLE)
admin.site.register(SCHEDULED_PUSH_TABLE)
admin.site.register(PUSH_HISTORY_TABLE)