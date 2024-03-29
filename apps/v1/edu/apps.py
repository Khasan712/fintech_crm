from django.apps import AppConfig


class EduConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.edu'
    label = 'edu'

    def ready(self):
        try:
            from apps.v1.edu import signals
        except ImportError:
            pass
