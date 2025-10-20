from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for managing and viewing staff profiles.
    Includes user metadata for convenience and admin controls for privileges.
    """
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="full_name", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "user",
            "username",
            "email",
            "full_name",
            "position",
            "department",
            "phone",
            "hired_on",
            "can_approve_loans",
            "can_approve_savings",
            "is_active",
        ]
        read_only_fields = ["id", "username", "email", "full_name", "hired_on"]
