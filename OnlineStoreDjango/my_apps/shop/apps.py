from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_apps.shop"

    def ready(self):
        import my_apps.shop.signals
