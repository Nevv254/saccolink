from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, LoanRepaymentViewSet

# Router setup
router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'repayments', LoanRepaymentViewSet, basename='loan-repayment')

urlpatterns = [
    # Include all viewset routes
    path('', include(router.urls)),

    # (Optional) You can add specific custom endpoints here in the future:
    # path('loans/<int:pk>/summary/', LoanSummaryView.as_view(), name='loan-summary'),
]
