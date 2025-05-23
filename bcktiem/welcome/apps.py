# apps.py
from django.apps import AppConfig

class WelcomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'welcome'

    def ready(self):
        import welcome.signals