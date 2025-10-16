from rest_framework import serializers
from .models import Loan, LoanRepayment

class LoanSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.username', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'member', 'member_name', 'amount', 'interest_rate',
            'duration_months', 'status', 'requested_on',
            'approved_on', 'due_date', 'balance'
        ]
        read_only_fields = ['status', 'approved_on', 'balance']


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ['id', 'loan', 'amount', 'date']
