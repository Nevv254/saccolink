from rest_framework import serializers
from apps.accounts.models import User
from .models import Member

# Nested User Serializer for member info
class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

# Main Member Serializer
class MemberSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'address', 'national_id', 'date_of_birth', 'joined_at']
