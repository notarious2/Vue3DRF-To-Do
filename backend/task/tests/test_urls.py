from django.test import TestCase
from task.views import TaskViewAPI, TaskDetailAPI, TaskUpdatePriorityAPI
from django.urls import reverse, resolve
from user.models import User
from task.models import Task


class TestTaskUrls(TestCase):
    """Test that Task URLs are resolved"""

    def test_get_tasks_url_is_resolved(self):
        """Test that url to get tasks/get is resolved"""
        url = reverse("get_tasks")
        self.assertEqual(resolve(url).func.view_class, TaskViewAPI)

    def test_change_tasks_url_is_resolved(self):
        """Test that url to update tasks/patch is resolved"""

        # create a task to pass task_id as an argument/path variable
        user = User.objects.create_user(email="test@example.com", username="testuser")
        task_id = Task.objects.create(priority=1, text="test task", user=user).task_id

        url = reverse("change_tasks", args=[task_id])
        self.assertEqual(resolve(url).func.view_class, TaskDetailAPI)

    def test_change_tasks_url_is_resolved(self):
        """Test that url to update priority of tasks/patch is resolved"""
        url = reverse("update_priority")
        self.assertEqual(resolve(url).func.view_class, TaskUpdatePriorityAPI)
