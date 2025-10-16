from django.urls import path
from .views import DepositViewSet, WithdrawalViewSet

urlpatterns = [
    # Deposit endpoints
    path('deposits/', DepositViewSet.as_view({
        'get': 'list',        # View deposits
        'post': 'create'      # Make deposit
    }), name='deposit-list-create'),

    # Withdrawal endpoints
    path('withdrawals/', WithdrawalViewSet.as_view({
        'get': 'list',        # View withdrawals
        'post': 'create'      # Make withdrawal
    }), name='withdrawal-list-create'),
]
