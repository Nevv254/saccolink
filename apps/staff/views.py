from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Staff
from .serializers import StaffSerializer

try:
    from apps.accounts.permissions import IsAdmin
    admin_perm = IsAdmin
except Exception:
    from rest_framework.permissions import IsAdminUser as admin_perm


class StaffViewSet(viewsets.ModelViewSet):
    """
    Staff Management API:
    - Admins can create, view, update, or delete staff records.
    - Regular staff can only view or update their own profile.
    - Includes an extra endpoint to toggle staff active status or privileges.
    """
    queryset = Staff.objects.select_related("user").all()
    serializer_class = StaffSerializer
    permission_classes = [admin_perm]

    def get_queryset(self):
        """Admins see all staff, regular staff only see their own record."""
        user = self.request.user
        if hasattr(user, "role") and user.role.lower() == "admin":
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        """Ensure staff record always links to a user with the STAFF role."""
        user = serializer.validated_data["user"]
        if hasattr(user, "role") and user.role.lower() != "staff":
            user.role = "STAFF"
            user.save()
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[admin_perm])
    def toggle_active(self, request, pk=None):
        """
        Admin-only endpoint to activate or deactivate a staff account.
        """
        staff = self.get_object()
        staff.is_active = not staff.is_active
        staff.save()
        return Response(
            {"message": f"Staff '{staff.user.username}' active status set to {staff.is_active}."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], permission_classes=[admin_perm])
    def set_privileges(self, request, pk=None):
        """
        Admin-only endpoint to update staff privileges (loan/savings approval).
       
        """
        staff = self.get_object()
        can_approve_loans = request.data.get("can_approve_loans", staff.can_approve_loans)
        can_approve_savings = request.data.get("can_approve_savings", staff.can_approve_savings)

        staff.can_approve_loans = can_approve_loans
        staff.can_approve_savings = can_approve_savings
        staff.save()

        return Response(
            {"message": f"Updated privileges for {staff.user.username}.",
             "can_approve_loans": staff.can_approve_loans,
             "can_approve_savings": staff.can_approve_savings},
            status=status.HTTP_200_OK
        )
