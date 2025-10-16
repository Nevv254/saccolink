from rest_framework import generics, permissions
from .models import Savings
from .serializers import SavingsSerializer
from .permissions import IsMemberOrAdmin

class SavingsListCreateView(generics.ListCreateAPIView):
    """
    GET: Admin/Staff - view all savings
    POST: Member - add new savings
    """
    serializer_class = SavingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsMemberOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'staff']:
            return Savings.objects.all()
        return Savings.objects.filter(member__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(member=user.member_profile)
