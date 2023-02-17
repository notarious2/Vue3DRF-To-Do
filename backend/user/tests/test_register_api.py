from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class TestRegistrationAPI(TestCase):
    """Test RegistrationAPI to create a user"""

    def setUp(self):
        self.client = APIClient()

    def test_register_new_user_success(self):
        """Test user creation with POST request"""
        payload = {
            "email": "example@test.com",
            "username": "testusername",
            "password": "testpassword",
        }
        url = reverse("register")
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "User has been created")

    def test_register_new_user_invalid_email(self):
        """Test user creation with invalid email input"""
        payload = {
            "email": "notanemail",
            "username": "testusername",
            "password": "testpassword",
        }
        url = reverse("register")

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address", str(response.data))

    def test_register_new_user_username_and_email_exist(self):
        """Test user creation with existing email"""

        payload = {"email": "example@test.com", "username": "test", "password": "test"}
        User.objects.create(**payload)
        url = reverse("register")

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this email already exists", str(response.data))
        self.assertIn("user with that username already exists", str(response.data))
