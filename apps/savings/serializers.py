from rest_framework import serializers
from .models import Savings

class SavingsSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.username', read_only=True)

    class Meta:
        model = Savings
        fields = ['id', 'member', 'member_name', 'amount', 'description', 'date']
        read_only_fields = ['date', 'member_name']
