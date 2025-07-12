from django.apps import AppConfig


class ShopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shops'

    def ready(self):
        import shops.signals
        return super().ready()
