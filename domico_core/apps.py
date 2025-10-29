from django.apps import AppConfig


class DomicoCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domico_core'

    # def ready(self):
    #     import domico_core.signals  

