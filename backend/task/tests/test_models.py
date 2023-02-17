from django.test import TestCase
from task.models import Task
from user.models import User


class TestTaskModel(TestCase):
    """Test task model"""

    def test_create_task_user(self):
        """Test task creation by registered user"""
        user = User.objects.create_user(email="test@example.com", username="testuser")
        task = Task.objects.create(priority=1, text="test task", user=user)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.user, user)
        self.assertEqual(task.text, "test task")
        self.assertEqual(str(task), "test task by testuser")
