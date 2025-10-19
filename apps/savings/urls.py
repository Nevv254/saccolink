from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, WithdrawalViewSet, BalanceView

# Use DRF's router to automatically generate routes
router = DefaultRouter()
router.register(r'deposits', DepositViewSet, basename='deposit')
router.register(r'withdrawals', WithdrawalViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
    path('balance/', BalanceView.as_view(), name='member-balance'),
]
