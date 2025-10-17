from django.db import models
from django.conf import settings

class Staff(models.Model):
    """
    Metadata for staff members. Each Staff links one-to-one with a User who has role='STAFF'.
    Keep business approval references on Loan/Savings as FK to User for simplicity.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )
    position = models.CharField(max_length=128, blank=True)
    department = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    hired_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.position or 'Staff'})"
