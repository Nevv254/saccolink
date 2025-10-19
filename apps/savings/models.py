from django.db import models
from django.conf import settings
from apps.members.models import Member


class Deposit(models.Model):
    """
    Represents a deposit transaction made by a member.
    Workflow:
      - Member creates → status='pending'
      - Admin approves/rejects → updates status, approved_by, approved_on
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    # Approval fields
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_deposits"
    )
    approved_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Deposit {self.amount} by {self.member.user.username} ({self.status})"


class Withdrawal(models.Model):
    """
    Represents a withdrawal transaction made by a member.
    Workflow:
      - Member requests → status='pending'
      - Admin approves/rejects → updates status, approved_by, approved_on
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    # Approval fields
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_withdrawals"
    )
    approved_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Withdrawal {self.amount} by {self.member.user.username} ({self.status})"
