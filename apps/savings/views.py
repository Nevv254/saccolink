from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.utils import timezone
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from apps.members.models import Member


class IsAdminOrMember(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins: access all records
    - Members: only access their own
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


class DepositViewSet(viewsets.ModelViewSet):
    """
    Handles deposit creation, listing, and admin approval/rejection.
    """
    queryset = Deposit.objects.all().order_by('-created_at')
    serializer_class = DepositSerializer
    permission_classes = [IsAdminOrMember]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin can view all deposits
            return Deposit.objects.all().order_by('-created_at')
        return Deposit.objects.filter(member=user.member_profile).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Member creates a deposit (starts as pending).
        """
        member = self.request.user.member_profile
        serializer.save(member=member, status="pending")

    # ---- ADMIN ACTIONS ----
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Admin approves a pending deposit.
        """
        deposit = self.get_object()
        if deposit.status != "pending":
            return Response({"detail": "Deposit already processed."}, status=status.HTTP_400_BAD_REQUEST)

        deposit.status = "approved"
        deposit.approved_by = request.user
        deposit.approved_on = timezone.now()
        deposit.save()

        # Update member’s balance
        deposit.member.savings_balance += deposit.amount
        deposit.member.save()

        return Response({"detail": f"Deposit #{deposit.id} approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Admin rejects a pending deposit.
        """
        deposit = self.get_object()
        if deposit.status != "pending":
            return Response({"detail": "Deposit already processed."}, status=status.HTTP_400_BAD_REQUEST)

        deposit.status = "rejected"
        deposit.approved_by = request.user
        deposit.approved_on = timezone.now()
        deposit.save()

        return Response({"detail": f"Deposit #{deposit.id} rejected."}, status=status.HTTP_200_OK)


class WithdrawalViewSet(viewsets.ModelViewSet):
    """
    Handles withdrawal creation, listing, and admin approval/rejection.
    """
    queryset = Withdrawal.objects.all().order_by('-created_at')
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAdminOrMember]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Withdrawal.objects.all().order_by('-created_at')
        return Withdrawal.objects.filter(member=user.member_profile).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Member requests a withdrawal (starts as pending).
        """
        member = self.request.user.member_profile
        if serializer.validated_data['amount'] > member.savings_balance:
            return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(member=member, status="pending")

    # ---- ADMIN ACTIONS ----
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Admin approves a pending withdrawal.
        """
        withdrawal = self.get_object()
        if withdrawal.status != "pending":
            return Response({"detail": "Withdrawal already processed."}, status=status.HTTP_400_BAD_REQUEST)

        member = withdrawal.member
        if withdrawal.amount > member.savings_balance:
            return Response({"error": "Insufficient funds to approve withdrawal."}, status=status.HTTP_400_BAD_REQUEST)

        withdrawal.status = "approved"
        withdrawal.approved_by = request.user
        withdrawal.approved_on = timezone.now()
        withdrawal.save()

        # Deduct amount from member balance
        member.savings_balance -= withdrawal.amount
        member.save()

        return Response({"detail": f"Withdrawal #{withdrawal.id} approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Admin rejects a pending withdrawal.
        """
        withdrawal = self.get_object()
        if withdrawal.status != "pending":
            return Response({"detail": "Withdrawal already processed."}, status=status.HTTP_400_BAD_REQUEST)

        withdrawal.status = "rejected"
        withdrawal.approved_by = request.user
        withdrawal.approved_on = timezone.now()
        withdrawal.save()

        return Response({"detail": f"Withdrawal #{withdrawal.id} rejected."}, status=status.HTTP_200_OK)


class BalanceView(APIView):
    """
    Endpoint to check a member's total savings balance.
    - Members see their own balance.
    - Admins can view all members’ balances.
    """

    def get(self, request):
        user = request.user

        if not user.is_staff:
            member = getattr(user, "member_profile", None)
            if not member:
                return Response({"error": "No member profile found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                "member": user.username,
                "balance": member.savings_balance
            })

        # Admin → all members’ balances
        all_members = Member.objects.all().values("user__username", "savings_balance")
        return Response({
            "total_members": all_members.count(),
            "balances": list(all_members)
        })
