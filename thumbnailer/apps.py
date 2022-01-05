from django.apps import AppConfig


class ThumbnailerConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'thumbnailer'

    def ready(self):
        import thumbnailer.signals
