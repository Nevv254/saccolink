from django.urls import path
from .views import MemberListView, MemberDetailView, MyProfileView

urlpatterns = [
    path('', MemberListView.as_view(), name='member-list'),
    path('<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('me/', MyProfileView.as_view(), name='member-profile'),
]
