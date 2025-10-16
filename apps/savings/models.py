from django.db import models
from apps.members.models import Member


class Deposit(models.Model):
    """
    Represents a deposit transaction made by a member.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit of {self.amount} by {self.member.user.username}"


class Withdrawal(models.Model):
    """
    Represents a withdrawal transaction made by a member.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal of {self.amount} by {self.member.user.username}"
