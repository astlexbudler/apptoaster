from django.apps import AppConfig
from .services import scheduler

class IntegratedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrated'

    # apscheduler
    def ready(self):
        scheduler.startScheduler()