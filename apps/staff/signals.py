from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.staff.models import Staff
from django.apps import apps

User = apps.get_model(settings.AUTH_USER_MODEL)

@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    """
    When a User is created or updated and their role is 'STAFF', ensure a Staff record exists.
    If role changes away from STAFF, optional: delete staff profile (or keep for audit).
    """
    try:
        role = getattr(instance, "role", "").lower()
    except Exception:
        role = ""

    if role == "staff":
        # create if not exists
        Staff.objects.get_or_create(user=instance)
