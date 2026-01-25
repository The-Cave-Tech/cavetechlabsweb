from django.apps import AppConfig


class CavetechappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cavetechapp'
    verbose_name = 'Cave Tech Application'

    def ready(self):
        """Register signals when app is ready."""
        import cavetechapp.signals