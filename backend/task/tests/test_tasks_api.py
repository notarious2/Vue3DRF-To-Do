"""
Test for task APIs
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from task.models import Task
from user.models import User
from task.serializers import TaskSerializer


class TaskAPITests(TestCase):
    """Test task APIs"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser")
        self.user_2 = User.objects.create_user(
            email="test2@example.com", username="testuser2")

    def test_get_tasks_unauthorized(self):
        """Test getting tasks by unauthorized user"""
        url = reverse('get_tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks_authorized_no_tasks(self):
        """Test getting tasks by authorized user with no tasks"""
        url = reverse('get_tasks')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_tasks_authorized_with_tasks(self):
        """Test getting tasks by authorized user with tasks"""
        # create test tasks
        Task.objects.create(
            priority=1, text='test task 1', user=self.user)
        Task.objects.create(
            priority=2, text='test task 2', user=self.user)

        tasks = Task.objects.filter(user=self.user)
        task_serializer = TaskSerializer(tasks, many=True)
        url = reverse('get_tasks')
        # authenticate the client
        self.client.force_authenticate(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task_serializer.data, response.data)

    def test_get_tasks_authorized_with_tasks(self):
        """Test getting OWN tasks by authorized user with tasks"""
        # create test task for user
        Task.objects.create(
            priority=1, text='test task 1', user=self.user)
        # create task for another user
        Task.objects.create(
            priority=2, text='test task 1', user=self.user_2)

        tasks = Task.objects.filter(user=self.user)
        task_serializer = TaskSerializer(tasks, many=True)
        url = reverse('get_tasks')
        # authenticate the client
        self.client.force_authenticate(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task_serializer.data, response.data)

    def test_POST_create_task_unauthorized(self):
        """Test POST request to create task by unauthorized user"""

        url = reverse('get_tasks')
        payload = {
            'priority': 1,
            'text': 'test task 1',
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_POST_create_task_authorized_invalid(self):
        """Test POST request to create a task (invalid data passed) by authorized user"""

        url = reverse('get_tasks')
        payload = {
            'priority': True,  # incorrect input
            'text': 'test task 1',
        }
        # authenticate the client
        self.client.force_authenticate(self.user)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POST_create_task_authorized_valid(self):
        """Test POST request to create a task (valid data passed) by authorized user"""

        url = reverse('get_tasks')
        payload = {
            'priority': 1,
            'text': 'test task 1',
        }
        # authenticate the client
        self.client.force_authenticate(self.user)
        response = self.client.post(url, payload)

        tasks = Task.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(payload['text'], tasks[0].text)
