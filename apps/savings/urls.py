from django.urls import path
from .views import SavingsListCreateView

urlpatterns = [
    path('', SavingsListCreateView.as_view(), name='savings-list-create'),
]
