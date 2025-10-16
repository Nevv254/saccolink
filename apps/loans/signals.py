from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan

@receiver(post_save, sender=Loan)
def set_loan_balance(sender, instance, created, **kwargs):
    """
    Automatically calculate total loan balance when approved.
    """
    if created and instance.status == 'approved':
        principal = instance.amount
        interest = (instance.interest_rate / 100) * principal
        total = principal + interest
        instance.balance = total
        instance.save()
