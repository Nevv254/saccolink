from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwner(BasePermission):
    """
    Allow admins to access everything, 
    but members only their own objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return hasattr(obj, "member") and obj.member.user == request.user


class IsAdminUser(BasePermission):
    """
    Restrict certain actions (like approval/rejection) to admins only.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
