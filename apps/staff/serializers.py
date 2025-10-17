from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    # show username and email for easy admin lookup
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Staff
        fields = ["id", "user", "username", "email", "position", "department", "phone", "hired_on"]
        read_only_fields = ["id", "username", "email", "hired_on"]
