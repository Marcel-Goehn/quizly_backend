from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester.mail@test.com",
                                             password="test12345")

    def test_register_successful(self):
        url = reverse("register")
        data = {
            "username": "testname",
            "password": "test12345",
            "confirmed_password": "test12345",
            "email": "your_test@example.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_username_already_exists(self):
        url = reverse("register")
        data = {
            "username": "tester",
            "password": "test12345",
            "repeated_password": "test12345",
            "email": "testingmailer@mail.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_email_already_exists(self):
        url = reverse("register")
        data = {
            "username": "testname",
            "password": "test12345",
            "repeated_password": "test12345",
            "email": "tester.mail@test.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_successfully(self):
        url = reverse("login")
        data = {
            "username": "tester",
            "password": "test12345"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_not_successful(self):
        url = reverse("login")
        data = {
            "username": "tester",
            "password": "test1234"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_successfully(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("logout")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_authenticated(self):
        url = reverse("logout")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)