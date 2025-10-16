from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Savings

@receiver(post_save, sender=Savings)
def update_member_balance(sender, instance, created, **kwargs):
    """
    Automatically update member's balance when a new saving record is created.
    """
    if created:
        member = instance.member
        # Calculate total balance from all deposits
        total_savings = sum(s.amount for s in member.savings.all())
        member.savings_balance = total_savings
        member.save()
        print(f"Updated savings balance for {member.user.username}: {total_savings}")