from django.db import models
from django.conf import settings


class Staff(models.Model):
    """
    Represents a Sacco staff member. 
    Each Staff is linked one-to-one with a Django User account.
    Staff users can handle approvals for loans, deposits, and withdrawals.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )
    position = models.CharField(max_length=128, default="Staff")
    department = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    hired_on = models.DateField(auto_now_add=True)

    # Permission flags
    can_approve_loans = models.BooleanField(default=True)
    can_approve_savings = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
        ordering = ["-hired_on"]

    def __str__(self):
        return f"{self.user.username} - {self.position or 'Staff'}"

    @property
    def full_name(self):
        """Returns the staff's full name from the linked user model."""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    @property
    def email(self):
        """Shortcut to access email from user."""
        return self.user.email
