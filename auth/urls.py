from django.urls import path
from auth.views import LoginView, SignupView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("signup/", SignupView.as_view(), name="auth_register"),
]
