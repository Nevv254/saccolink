from rest_framework import generics, permissions
from .models import Member
from .serializers import MemberSerializer
from .permissions import IsAdminOrStaff

# --- Admin/Staff: View all members ---
class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrStaff]

# --- Admin/Staff: View individual member details ---
class MemberDetailView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrStaff]

# --- Member: View own profile ---
class MyProfileView(generics.RetrieveAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.member_profile
