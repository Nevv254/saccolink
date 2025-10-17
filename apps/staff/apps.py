from django.apps import AppConfig

class StaffConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.staff"

    def ready(self):
        # import signals so they are registered at app ready
        import apps.staff.signals  
