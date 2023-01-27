from django.apps import AppConfig
from django.conf import settings

class IntegratedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrated'

    # apscheduler
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from .services import scheduler
            scheduler.startScheduler()