from django.db import models
from django.conf import settings
from apps.members.models import Member

class Savings(models.Model):
    """
    Represents a member's savings deposit record.
    Each deposit updates the member's overall savings balance.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="savings")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.member.user.username} - Deposit: {self.amount}"
