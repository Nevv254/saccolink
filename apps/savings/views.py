from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from apps.members.models import Member


class IsAdminOrMemberOwner(permissions.BasePermission):
    """
    Custom permission:
    - Admins can view/manage all deposits & withdrawals.
    - Members can only view/manage their own.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        # Allow access only if this transaction belongs to the user's member profile
        return hasattr(request.user, "member_profile") and obj.member == request.user.member_profile


class DepositViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for deposits.
    Automatically links deposit to the logged-in member.
    """
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [IsAdminOrMemberOwner]

    def get_queryset(self):
        user = self.request.user
        # Admins see all deposits
        if user.role == "admin":
            return Deposit.objects.all()
        # Members only see their deposits
        if hasattr(user, "member_profile"):
            return Deposit.objects.filter(member=user.member_profile)
        return Deposit.objects.none()

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user's member profile to the deposit.
        """
        user = self.request.user
        try:
            member = Member.objects.get(user=user)
        except Member.DoesNotExist:
            raise ValueError("No member profile found for this user.")
        serializer.save(member=member)


class WithdrawalViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for withdrawals.
    Automatically links withdrawal to the logged-in member.
    """
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAdminOrMemberOwner]

    def get_queryset(self):
        user = self.request.user
        # Admins see all withdrawals
        if user.role == "admin":
            return Withdrawal.objects.all()
        # Members only see their own withdrawals
        if hasattr(user, "member_profile"):
            return Withdrawal.objects.filter(member=user.member_profile)
        return Withdrawal.objects.none()

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user's member profile to the withdrawal.
        """
        user = self.request.user
        try:
            member = Member.objects.get(user=user)
        except Member.DoesNotExist:
            raise ValueError("No member profile found for this user.")
        serializer.save(member=member)
