# Auth Views
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, SignupSerializer


class LoginView(TokenObtainPairView):
    """
    LoginView class
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class SignupView(generics.CreateAPIView):
    """
    SignupView class
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


def get_health(request):
    """
    HealthCheck request
    """
    return JsonResponse({"status": "Ok!"}, status=200)
