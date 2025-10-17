from django.urls import path
from .views import AdminDashboardAPIView

urlpatterns = [
    path("dashboard/", AdminDashboardAPIView.as_view(), name="admin-dashboard"),
]
