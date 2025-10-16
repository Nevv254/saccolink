from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Loan, LoanRepayment
from .serializers import LoanSerializer, LoanRepaymentSerializer
from apps.members.models import Member


class LoanViewSet(viewsets.ModelViewSet):
    """
    Handles loan applications, viewing, and admin approval.
    """
    queryset = Loan.objects.all().order_by('-requested_on')
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin sees all loans
            return Loan.objects.all().order_by('-requested_on')
        # Member sees only their own loans
        try:
            member = Member.objects.get(user=user)
            return Loan.objects.filter(member=member).order_by('-requested_on')
        except Member.DoesNotExist:
            return Loan.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        try:
            member = Member.objects.get(user=user)
            serializer.save(member=member)
        except Member.DoesNotExist:
            raise ValueError("Member record not found for this user.")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Admin-only: Approve a pending loan.
        """
        loan = self.get_object()
        if loan.status != 'pending':
            return Response({'detail': 'Loan already processed.'}, status=status.HTTP_400_BAD_REQUEST)

        loan.status = 'approved'
        loan.approved_on = timezone.now()
        loan.due_date = timezone.now().date().replace(year=timezone.now().year + 1)
        loan.save()
        return Response({'detail': f'Loan #{loan.id} approved successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Admin-only: Reject a pending loan.
        """
        loan = self.get_object()
        if loan.status != 'pending':
            return Response({'detail': 'Loan already processed.'}, status=status.HTTP_400_BAD_REQUEST)

        loan.status = 'rejected'
        loan.save()
        return Response({'detail': f'Loan #{loan.id} rejected.'}, status=status.HTTP_200_OK)


class LoanRepaymentViewSet(viewsets.ModelViewSet):
    """
    Handles recording and viewing of loan repayments.
    """
    queryset = LoanRepayment.objects.all().order_by('-date')
    serializer_class = LoanRepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LoanRepayment.objects.all().order_by('-date')
        try:
            member = Member.objects.get(user=user)
            return LoanRepayment.objects.filter(loan__member=member).order_by('-date')
        except Member.DoesNotExist:
            return LoanRepayment.objects.none()

    def perform_create(self, serializer):
        repayment = serializer.save()
        loan = repayment.loan
        loan.balance -= repayment.amount

        if loan.balance <= 0:
            loan.balance = 0
            loan.status = 'completed'
        loan.save()
