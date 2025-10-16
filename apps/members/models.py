from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Member(models.Model):
    """
    Member profile linked to a user.
    Automatically created when a user with role='member' registers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member_profile")
    address = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    savings_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    loan_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Member Profile: {self.user.username}"
