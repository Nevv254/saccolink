from rest_framework import permissions

class IsAdminOrStaff(permissions.BasePermission):
    """
    Allow access only to Admin or Staff users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ["ADMIN", "STAFF"]
        )
