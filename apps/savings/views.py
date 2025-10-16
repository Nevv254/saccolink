from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from rest_framework.views import APIView
from rest_framework import status


class IsAdminOrMember(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins: access all records
    - Members: only access their own
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [IsAdminOrMember]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin → view all
            return Deposit.objects.all()
        return Deposit.objects.filter(member=user.member_profile)

    def perform_create(self, serializer):
        member = self.request.user.member_profile
        serializer.save(member=member)


class WithdrawalViewSet(viewsets.ModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAdminOrMember]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Withdrawal.objects.all()
        return Withdrawal.objects.filter(member=user.member_profile)

    def perform_create(self, serializer):
        member = self.request.user.member_profile
        serializer.save(member=member)


# After saving the withdrawal, update the member's balance
class BalanceView(APIView):
    """
    Endpoint to check a member's total savings balance.
    - Members see their own balance.
    - Admins can view all members’ balances.
    """

    def get(self, request):
        user = request.user

        # Member → only view own balance
        if not user.is_staff:
            member = getattr(user, "member_profile", None)
            if not member:
                return Response(
                    {"error": "No member profile found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({
                "member": user.username,
                "balance": member.savings_balance
            })

        # Admin → view all members’ balances
        from apps.members.models import Member
        all_members = Member.objects.all().values("user__username", "savings_balance")

        return Response({
            "total_members": all_members.count(),
            "balances": list(all_members)
        })

