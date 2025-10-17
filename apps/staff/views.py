from rest_framework import viewsets, permissions
from .models import Staff
from .serializers import StaffSerializer

# Use your project-specific IsAdmin if you have it:
try:
    from apps.accounts.permissions import IsAdmin  # adjust import to where you store the permission
    admin_perm = IsAdmin
except Exception:
    from rest_framework.permissions import IsAdminUser as admin_perm

class StaffViewSet(viewsets.ModelViewSet):
    """
    Admins can create, view, update, delete staff meta-records.
    Regular staff can view their own profile (handled implicitly via queryset filtering).
    """
    queryset = Staff.objects.select_related("user").all()
    serializer_class = StaffSerializer
    permission_classes = [admin_perm]

    def get_queryset(self):
        # Staff can only view their own profile; admins see all.
        user = self.request.user
        if user and getattr(user, "role", "").lower() == "admin":
            return self.queryset
        return self.queryset.filter(user=user)
