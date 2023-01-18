from django.apps import AppConfig
from . import utilities

class IntegratedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrated'

    # apscheduler
    def ready(self):
        utilities.startScheduler()