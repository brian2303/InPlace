from django.urls import path
from apps.login.views import LoginFormView,DashboardView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',LoginFormView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='index'),name='logout'),
]