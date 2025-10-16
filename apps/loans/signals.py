from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, LoanRepayment
from apps.members.models import Member

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


# When a loan is approved → update the member's loan balance
@receiver(post_save, sender=Loan)
def update_member_balance_on_approval(sender, instance, created, **kwargs):
    if instance.status == 'approved':  # Only update when loan is approved
        member = instance.member
        member.loan_balance += instance.amount
        member.save()


#  When a repayment is made → reduce member's loan balance
@receiver(post_save, sender=LoanRepayment)
def update_member_balance_on_repayment(sender, instance, created, **kwargs):
    if created:
        loan = instance.loan
        member = loan.member
        # Reduce the outstanding balance on both the loan and the member
        loan.balance -= instance.amount
        if loan.balance < 0:
            loan.balance = 0
        loan.save()

        member.loan_balance -= instance.amount
        if member.loan_balance < 0:
            member.loan_balance = 0
        member.save()


