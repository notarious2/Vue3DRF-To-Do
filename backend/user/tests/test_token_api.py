from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User
from task.models import Task


class TestJWTAPIs(TestCase):
    """Test JWT Token APIs to create/refresh tokens"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )
        # self.client.force_authenticate(self.user)

    def test_jwt_create_token_valid_username(self):
        """Test creating JWT access and refresh tokens with valid username/password"""
        url = reverse("jwt-create")
        response = self.client.post(
            url, data={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_jwt_create_token_valid_email(self):
        """Test creating JWT access and refresh tokens with valid email/password"""
        url = reverse("jwt-create")
        response = self.client.post(
            url, data={"username": "test@example.com",
                       "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_jwt_create_token_invalid(self):
        """Test creating JWT access and refresh tokens with invalid credentials"""
        url = reverse("jwt-create")
        response = self.client.post(
            url, data={"username": "testuser", "password": "wrongpassword"}
        )

        self.assertIn(
            "No active account found with the given credentials", str(
                response.data)
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_refresh_token_invalid_refresh(self):
        """Test refresh token API with invalid refresh token"""
        url = reverse("jwt-refresh")
        response = self.client.post(url, data={"refresh": "invalidtoken"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is invalid", str(response.data))

    def test_jwt_refresh_token_success(self):
        """Test refresh token API with invalid refresh token"""
        create_url = reverse("jwt-create")
        refresh_url = reverse("jwt-refresh")

        # obtain refresh token from jwt-create
        get_tokens = self.client.post(
            create_url, data={"username": "testuser",
                              "password": "testpassword"}
        )
        refresh_token = get_tokens.data["refresh"]

        # obtain new access token
        response = self.client.post(
            refresh_url, data={"refresh": refresh_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
