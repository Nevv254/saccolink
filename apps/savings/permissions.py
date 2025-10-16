from rest_framework.permissions import BasePermission

class IsMemberOrAdmin(BasePermission):
    """
    - Members: can view their own savings and add deposits.
    - Staff/Admin: can view all savings.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role in ['member', 'staff', 'admin']

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Members can only access their own savings
        if user.role == 'member':
            return obj.member.user == user
        return True
