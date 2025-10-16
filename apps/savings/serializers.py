from rest_framework import serializers
from .models import Deposit, Withdrawal


class DepositSerializer(serializers.ModelSerializer):
    """
    Serializer for deposits:
    - Member is automatically linked (read-only).
    - Shows deposit amount and date.
    """
    member = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Deposit
        fields = ['id', 'member', 'amount', 'date']
        read_only_fields = ['id', 'member', 'date']


class WithdrawalSerializer(serializers.ModelSerializer):
    """
    Serializer for withdrawals:
    - Member is automatically linked (read-only).
    - Shows withdrawal amount and date.
    """
    member = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Withdrawal
        fields = ['id', 'member', 'amount', 'date']
        read_only_fields = ['id', 'member', 'date']
