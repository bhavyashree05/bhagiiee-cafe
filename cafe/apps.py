from django.apps import AppConfig


class CafeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cafe"
    verbose_name = "Coffee Machine"

    def ready(self):
        try:
            from django.contrib.auth.models import User

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@gmail.com",
                    password="Admin@123",
                )
        except Exception:
            # Ignore errors during migrations/startup
            pass
