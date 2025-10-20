from django.urls import path
from .views import AdminDashboardAPIView, AnalyticsTrendsView, FinancialSummaryView, PerformanceMetricsView

urlpatterns = [
    path("dashboard/", AdminDashboardAPIView.as_view(), name="admin-dashboard"),
    path("trends/", AnalyticsTrendsView.as_view(), name="analytics-trends"),
    path("financials/", FinancialSummaryView.as_view(), name="analytics-financials"),
    path("performance/", PerformanceMetricsView.as_view(), name="analytics-performance"),
]
