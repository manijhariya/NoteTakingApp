from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

AUTH_SAMPLE_DATA = {
    "username": "johnwick",
    "password": "aB@#2022",
    "email": "abc@xyz.com",
    "first_name": "John",
    "last_name": "Wick",
}


class LoginAPITest(APITestCase):
    url = "/auth/login/"

    def setUp(self):
        user = User.objects.create_user(**AUTH_SAMPLE_DATA)

    def test_authenticated_user_login(self):
        data = {"username": "johnwick", "password": "aB@#2022"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_login_failed(self):
        data = {"username": "johnwick", "password": "aB@#202"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_username_field_required(self):
        data = {"username": "johnwick"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_password_field_required(self):
        data = {"password": "aB@#202"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SignUpAPITest(APITestCase):
    url = "/auth/signup/"

    def test_user_signup_successful(self):
        data = {**AUTH_SAMPLE_DATA, "password2": "aB@#2022"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_singup_all_field_required(self):
        data = {**AUTH_SAMPLE_DATA}

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Field is required failed",
        )

    def test_user_singup_pass_not_match(self):
        data = {**AUTH_SAMPLE_DATA}
        data["password2"] = "aC@#2022"

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Password1 and Password2 do not match.",
        )

    def test_user_singup_invalid_email(self):
        data = {**AUTH_SAMPLE_DATA, "password2": "aB@#2022"}
        data["email"] = "abc"

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Invalid Email Failed",
        )

    def test_user_singup_duplicate_username(self):
        user = User.objects.create_user(**AUTH_SAMPLE_DATA)

        data = {
            "username": "johnwick",
            "password": "aD@#2022",
            "password2": "aD@#2022",
            "email": "xyz@abc.com",
            "first_name": "John",
            "last_name": "Wick",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Duplicate username Failed.",
        )

    def test_user_singup_duplicate_email(self):
        user = User.objects.create_user(**AUTH_SAMPLE_DATA)

        data = {
            "username": "johnwick2",
            "password": "aD@#2022",
            "password2": "aD@#2022",
            "email": "abc@xyz.com",
            "first_name": "John",
            "last_name": "Wick",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Duplicate email Failed.",
        )
