from django.db import models
from django.conf import settings

# Each Member will be linked to one User (with role='MEMBER')
class Member(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="member_profile"
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Member Profile"
