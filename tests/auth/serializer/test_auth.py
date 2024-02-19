from django.test import TestCase
from auth.serializers import SignupSerializer, LoginSerializer
from django.contrib.auth.models import User

AUTH_SAMPLE_DATA = {
            "username": "johnwick",
            "password": "aB@#2022",
            "email": "abc@xyz.com",
            "first_name": "John",
            "last_name": "Wick",
        }

class AuthLoginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(**AUTH_SAMPLE_DATA)

    def test_serializer_login_valid_data(self):
        data = {'username': 'johnwick', "password" : "aB@#2022"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg="Login Failed...")

class AuthSignupTest(TestCase):
    def test_serializer_signup_valid_data(self):
        data = {**AUTH_SAMPLE_DATA, "password2" : "aB@#2022"}
        serializer = SignupSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg="Signup Failed...")
        
    
