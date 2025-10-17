from django.apps import apps
from django.db.models import Sum, Count, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from apps.accounts.permissions import IsAdmin  


class AdminDashboardAPIView(APIView):
    """
    Admin-only dashboard summary for SaccoLink.
    Returns aggregated totals and short leaderboards.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # Lazy-load models to avoid import/circular issues
        try:
            Member = apps.get_model("members", "Member")
        except LookupError:
            Member = None

        try:
            Deposit = apps.get_model("savings", "Deposit")
        except LookupError:
            Deposit = None

        try:
            Withdrawal = apps.get_model("savings", "Withdrawal")
        except LookupError:
            Withdrawal = None

        try:
            Loan = apps.get_model("loans", "Loan")
        except LookupError:
            Loan = None

        try:
            LoanRepayment = apps.get_model("loans", "LoanRepayment")
        except LookupError:
            LoanRepayment = None

        
        data = {}

        # Members count
        if Member:
            data["total_members"] = Member.objects.count()
        else:
            data["total_members"] = None

        # Deposits: count and sum
        if Deposit:
            deposits_agg = Deposit.objects.aggregate(
                total_deposits=Sum("amount"), deposits_count=Count("id")
            )
            data["total_deposits"] = deposits_agg["total_deposits"] or 0
            data["deposits_count"] = deposits_agg["deposits_count"] or 0
        else:
            data["total_deposits"] = None
            data["deposits_count"] = None

        # Withdrawals: count and sum
        if Withdrawal:
            withdrawals_agg = Withdrawal.objects.aggregate(
                total_withdrawals=Sum("amount"), withdrawals_count=Count("id")
            )
            data["total_withdrawals"] = withdrawals_agg["total_withdrawals"] or 0
            data["withdrawals_count"] = withdrawals_agg["withdrawals_count"] or 0
        else:
            data["total_withdrawals"] = None
            data["withdrawals_count"] = None

        # Loans: totals and statuses
        if Loan:
            total_loans = Loan.objects.aggregate(total_loan_amount=Sum("amount"))["total_loan_amount"] or 0
            loans_by_status = Loan.objects.values("status").annotate(count=Count("id"))
            status_counts = {item["status"]: item["count"] for item in loans_by_status}
            data["total_loans_amount"] = total_loans
            data["loans_status_counts"] = status_counts
        else:
            data["total_loans_amount"] = None
            data["loans_status_counts"] = None

        # Repayments: total
        if LoanRepayment:
            repayments_agg = LoanRepayment.objects.aggregate(total_repayments=Sum("amount"), repayments_count=Count("id"))
            data["total_repayments"] = repayments_agg["total_repayments"] or 0
            data["repayments_count"] = repayments_agg["repayments_count"] or 0
        else:
            data["total_repayments"] = None
            data["repayments_count"] = None

        # Top savers (by total deposit) 
        if Deposit:
            top_savers_qs = (
                Deposit.objects
                .values(member_username=F("member__user__username"))
                .annotate(total=Sum("amount"))
                .order_by("-total")[:5]
            )
            data["top_savers"] = [
                {"username": r["member_username"] or "unknown", "total_deposited": r["total"]} for r in top_savers_qs
            ]
        else:
            data["top_savers"] = None

        # Top borrowers (by outstanding balance) 
        if Loan:
            top_borrowers_qs = (
                Loan.objects
                .values(borrower_username=F("member__user__username"))
                .annotate(outstanding=Sum("balance"))
                .order_by("-outstanding")[:5]
            )
            data["top_borrowers"] = [
                {"username": r["borrower_username"] or "unknown", "outstanding_balance": r["outstanding"]} for r in top_borrowers_qs
            ]
        else:
            data["top_borrowers"] = None

        return Response(data, status=status.HTTP_200_OK)
