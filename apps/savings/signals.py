# apps/savings/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Deposit, Withdrawal
from apps.members.models import Member

@receiver(post_save, sender=Deposit)
def update_balance_after_deposit(sender, instance, created, **kwargs):
    """
    When a deposit is created, add the deposited amount
    to the member's savings balance.
    """
    if created:
        member = instance.member
        member.savings_balance += instance.amount
        member.save()

@receiver(post_save, sender=Withdrawal)
def update_balance_after_withdrawal(sender, instance, created, **kwargs):
    """
    When a withdrawal is created, deduct the withdrawn amount
    from the member's savings balance (if sufficient balance exists).
    """
    if created:
        member = instance.member

        # Only deduct if the balance is sufficient
        if member.savings_balance >= instance.amount:
            member.savings_balance -= instance.amount
            member.save()
        else:
            # Optional: handle insufficient funds
            # (In production you might raise a validation error instead)
            print(f"Insufficient funds for member {member.user.username}. Withdrawal not processed properly.")
