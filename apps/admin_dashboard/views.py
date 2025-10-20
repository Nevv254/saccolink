from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Sum, Count
from apps.members.models import Member
from apps.loans.models import Loan
from apps.savings.models import Deposit, Withdrawal
from apps.staff.models import Staff


class AdminOverviewView(APIView):
    """
    summary of the SACCO's overall activity.
    Accessible to admins only.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        try:
            total_members = Member.objects.count()
            active_members = Member.objects.filter(is_active=True).count()

            total_loans = Loan.objects.count()
            approved_loans = Loan.objects.filter(status="APPROVED").count()
            pending_loans = Loan.objects.filter(status="PENDING").count()
            total_loan_amount = Loan.objects.aggregate(total=Sum("amount"))["total"] or 0

            total_deposits = Deposit.objects.aggregate(total=Sum("amount"))["total"] or 0
            total_withdrawals = Withdrawal.objects.aggregate(total=Sum("amount"))["total"] or 0
            total_balance = total_deposits - total_withdrawals

            staff_count = Staff.objects.count()

            return Response({
                "members": {
                    "total": total_members,
                    "active": active_members
                },
                "loans": {
                    "total": total_loans,
                    "approved": approved_loans,
                    "pending": pending_loans,
                    "total_amount": total_loan_amount
                },
                "savings": {
                    "total_deposits": total_deposits,
                    "total_withdrawals": total_withdrawals,
                    "total_balance": total_balance
                },
                "staff": {
                    "total": staff_count
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
