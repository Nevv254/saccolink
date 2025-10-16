from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Member

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Member profile when a user with role='member' is registered.
    """
    if created and instance.role.lower() == 'member':
        Member.objects.create(user=instance)
