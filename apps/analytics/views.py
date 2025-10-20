from datetime import datetime, timedelta
from django.apps import apps
from django.db.models import Sum, Count, F
from django.utils.timezone import now
from rest_framework import status, permissions, views
from rest_framework.response import Response
from apps.accounts.permissions import IsAdmin


class AdminDashboardAPIView(views.APIView):
    """
    Admin-only dashboard summary for SaccoLink.
    Includes totals, loan status breakdowns, and top savers/borrowers.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        # Lazy-load models to avoid circular imports
        Member = apps.get_model("members", "Member")
        Deposit = apps.get_model("savings", "Deposit")
        Withdrawal = apps.get_model("savings", "Withdrawal")
        Loan = apps.get_model("loans", "Loan")
        LoanRepayment = apps.get_model("loans", "LoanRepayment")

        data = {}

        # Members
        data["total_members"] = Member.objects.count()

        # Deposits
        deposits_agg = Deposit.objects.aggregate(total=Sum("amount"), count=Count("id"))
        data["total_deposits"] = deposits_agg["total"] or 0
        data["deposits_count"] = deposits_agg["count"] or 0

        # Withdrawals
        withdrawals_agg = Withdrawal.objects.aggregate(total=Sum("amount"), count=Count("id"))
        data["total_withdrawals"] = withdrawals_agg["total"] or 0
        data["withdrawals_count"] = withdrawals_agg["count"] or 0

        # Loans
        total_loans = Loan.objects.aggregate(total=Sum("amount"))["total"] or 0
        data["total_loans_amount"] = total_loans
        status_counts = {
            item["status"]: item["count"]
            for item in Loan.objects.values("status").annotate(count=Count("id"))
        }
        data["loans_status_counts"] = status_counts

        # Repayments
        repayments_agg = LoanRepayment.objects.aggregate(total=Sum("amount"), count=Count("id"))
        data["total_repayments"] = repayments_agg["total"] or 0
        data["repayments_count"] = repayments_agg["count"] or 0

        # Leaderboards
        top_savers_qs = (
            Deposit.objects.values(member_username=F("member__user__username"))
            .annotate(total=Sum("amount"))
            .order_by("-total")[:5]
        )
        data["top_savers"] = [
            {"username": r["member_username"] or "unknown", "total_deposited": r["total"]}
            for r in top_savers_qs
        ]

        top_borrowers_qs = (
            Loan.objects.values(borrower_username=F("member__user__username"))
            .annotate(outstanding=Sum("balance"))
            .order_by("-outstanding")[:5]
        )
        data["top_borrowers"] = [
            {"username": r["borrower_username"] or "unknown", "outstanding_balance": r["outstanding"]}
            for r in top_borrowers_qs
        ]

        return Response(data, status=status.HTTP_200_OK)


class AnalyticsTrendsView(views.APIView):
    """
    Monthly activity trends: new members, loans, deposits, withdrawals.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        Member = apps.get_model("members", "Member")
        Deposit = apps.get_model("savings", "Deposit")
        Withdrawal = apps.get_model("savings", "Withdrawal")
        Loan = apps.get_model("loans", "Loan")

        current_year = now().year
        data = {"months": [], "new_members": [], "loans": [], "deposits": [], "withdrawals": []}

        for month in range(1, 13):
            start = datetime(current_year, month, 1)
            end = (datetime(current_year + (month == 12), (month % 12) + 1, 1)
                   - timedelta(days=1))

            data["months"].append(start.strftime("%b"))
            data["new_members"].append(Member.objects.filter(joined_on__range=[start, end]).count())
            data["loans"].append(Loan.objects.filter(requested_on__range=[start, end]).count())
            data["deposits"].append(
                Deposit.objects.filter(date__range=[start, end]).aggregate(Sum("amount"))["amount__sum"] or 0
            )
            data["withdrawals"].append(
                Withdrawal.objects.filter(date__range=[start, end]).aggregate(Sum("amount"))["amount__sum"] or 0
            )

        return Response(data, status=status.HTTP_200_OK)


class FinancialSummaryView(views.APIView):
    """
    Provides total loaned, repaid, savings, and outstanding balances.
    Supports date filters 
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        Loan = apps.get_model("loans", "Loan")
        LoanRepayment = apps.get_model("loans", "LoanRepayment")
        Deposit = apps.get_model("savings", "Deposit")
        Withdrawal = apps.get_model("savings", "Withdrawal")

        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")

        filters = {}
        if start_date and end_date:
            filters["requested_on__range"] = [start_date, end_date]

        total_loans = Loan.objects.filter(**filters).aggregate(Sum("amount"))["amount__sum"] or 0
        total_repaid = LoanRepayment.objects.aggregate(Sum("amount"))["amount__sum"] or 0
        total_savings = Deposit.objects.aggregate(Sum("amount"))["amount__sum"] or 0
        total_withdrawn = Withdrawal.objects.aggregate(Sum("amount"))["amount__sum"] or 0

        outstanding = total_loans - total_repaid
        approval_rate = (Loan.objects.filter(status="approved").count() / Loan.objects.count() * 100) if Loan.objects.exists() else 0

        return Response({
            "date_range": {"start": start_date, "end": end_date},
            "total_loans": total_loans,
            "total_repaid": total_repaid,
            "total_savings": total_savings,
            "total_withdrawn": total_withdrawn,
            "outstanding_balance": outstanding,
            "approval_rate": round(approval_rate, 2),
        }, status=status.HTTP_200_OK)
    

class PerformanceMetricsView(views.APIView):
    """
    Returns computed performance indicators and ratios
    for quick chart rendering on the admin dashboard.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        Loan = apps.get_model("loans", "Loan")
        LoanRepayment = apps.get_model("loans", "LoanRepayment")
        Deposit = apps.get_model("savings", "Deposit")

        # --- Totals ---
        total_loans = Loan.objects.aggregate(Sum("amount"))["amount__sum"] or 0
        total_repaid = LoanRepayment.objects.aggregate(Sum("amount"))["amount__sum"] or 0
        total_deposits = Deposit.objects.aggregate(Sum("amount"))["amount__sum"] or 0

        # --- Ratios ---
        loan_to_deposit_ratio = (total_loans / total_deposits * 100) if total_deposits > 0 else 0
        repayment_rate = (total_repaid / total_loans * 100) if total_loans > 0 else 0

        # --- Loan Statuses ---
        loan_status_counts = (
            Loan.objects.values("status").annotate(count=Count("id")).order_by()
        )
        active_loans = sum(i["count"] for i in loan_status_counts if i["status"] == "approved")
        closed_loans = sum(i["count"] for i in loan_status_counts if i["status"] == "repaid")

        # --- Savings Growth (last 2 months) ---
        current_month_start = now().replace(day=1)
        prev_month_end = current_month_start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(day=1)

        current_total = (
            Deposit.objects.filter(date__gte=current_month_start)
            .aggregate(Sum("amount"))["amount__sum"] or 0
        )
        previous_total = (
            Deposit.objects.filter(date__range=[prev_month_start, prev_month_end])
            .aggregate(Sum("amount"))["amount__sum"] or 0
        )

        savings_growth = (
            ((current_total - previous_total) / previous_total * 100)
            if previous_total > 0 else 0
        )

        # --- Loan Approval Trend (last 6 months) ---
        approval_trend = []
        for i in range(5, -1, -1):
            start = (now().replace(day=1) - timedelta(days=30 * i)).replace(day=1)
            end = (start + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

            total_month_loans = Loan.objects.filter(requested_on__range=[start, end]).count()
            approved_month_loans = Loan.objects.filter(
                requested_on__range=[start, end], status="approved"
            ).count()

            approval_rate = (
                approved_month_loans / total_month_loans * 100
                if total_month_loans > 0 else 0
            )
            approval_trend.append({
                "month": start.strftime("%b"),
                "approval_rate": round(approval_rate, 2)
            })

        # --- Response Payload ---
        return Response({
            "loan_to_deposit_ratio": round(loan_to_deposit_ratio, 2),
            "repayment_rate": round(repayment_rate, 2),
            "savings_growth_percent": round(savings_growth, 2),
            "active_loans": active_loans,
            "closed_loans": closed_loans,
            "approval_trend": approval_trend,
        }, status=status.HTTP_200_OK)