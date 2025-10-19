from rest_framework import serializers
from .models import Deposit, Withdrawal


class DepositSerializer(serializers.ModelSerializer):
    """
    Serializer for Deposit model.
    - Members can only create deposits (status auto = pending).
    - Admins can view approval details.
    """
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = Deposit
        fields = [
            'id',
            'member',
            'member_name',
            'amount',
            'status',
            'approved_by',
            'approved_by_name',
            'approved_on',
            'created_at'
        ]
        read_only_fields = ['status', 'approved_by', 'approved_on', 'member']

    def create(self, validated_data):
        """
        Automatically set deposit status to 'pending' when created.
        """
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class WithdrawalSerializer(serializers.ModelSerializer):
    """
    Serializer for Withdrawal model.
    - Members can only request withdrawals (status auto = pending).
    - Admins can approve/reject.
    """
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = Withdrawal
        fields = [
            'id',
            'member',
            'member_name',
            'amount',
            'status',
            'approved_by',
            'approved_by_name',
            'approved_on',
            'created_at'
        ]
        read_only_fields = ['status', 'approved_by', 'approved_on', 'member']

    def create(self, validated_data):
        """
        Automatically set withdrawal status to 'pending' when created.
        """
        validated_data['status'] = 'pending'
        return super().create(validated_data)
