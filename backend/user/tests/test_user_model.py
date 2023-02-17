from django.test import TestCase
from user.models import User


class TestTaskModel(TestCase):
    """Test user model"""

    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create(
            email="test@example.com", username="testuser", password="test_password"
        )

        self.assertEqual(str(user), "testuser")
        self.assertEqual(User.objects.all()[0].email, "test@example.com")
        self.assertEqual(User.objects.count(), 1)
