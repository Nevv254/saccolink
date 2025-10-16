from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Deposit, Withdrawal
from apps.members.models import Member


@receiver(post_save, sender=Deposit)
def update_balance_after_deposit(sender, instance, created, **kwargs):
    """Update member's savings balance after a deposit is made"""
    if created:
        member = instance.member
        member.savings_balance += instance.amount
        member.save()


@receiver(post_save, sender=Withdrawal)
def update_balance_after_withdrawal(sender, instance, created, **kwargs):
    """Update member's savings balance after a withdrawal is made"""
    if created:
        member = instance.member
        member.savings_balance -= instance.amount
        member.save()
