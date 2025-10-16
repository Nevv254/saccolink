from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    # Display related user information as a string (e.g. username)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'user', 'address', 'national_id', 'date_of_birth', 'joined_on']
