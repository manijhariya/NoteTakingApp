# Auth urls
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth.views import LoginView, SignupView, get_health

urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("signup/", SignupView.as_view(), name="auth_register"),
    path("healthcheck/", get_health, name="healthcheck"),
]
