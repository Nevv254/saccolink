from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allow access only to users with role == 'ADMIN'
    """
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'role', None) == 'ADMIN')

class IsStaffOrAdmin(permissions.BasePermission):
    """
    Allow staff or admin
    """
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, 'role', None) in ['STAFF', 'ADMIN'])
