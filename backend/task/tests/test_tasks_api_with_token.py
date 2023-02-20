"""
Test Task APIs with Bearer JWT token instead of forcing authentication
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from task.models import Task
from user.models import User
from task.serializers import TaskSerializer


class TestTaskViewAPI(TestCase):
    """Test TaskViewAPI that gets and creates tasks"""

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.client = APIClient()
        cls.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )
        cls.user_2 = User.objects.create_user(
            email="test2@example.com", username="testuser2"
        )

        access_token = cls.client.post(
            reverse("jwt-create"),
            data={"username": "testuser", "password": "testpassword"},
        ).data["access"]
        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    def test_get_tasks_unauthorized(self):
        """Test getting tasks by unauthorized user"""
        url = reverse("get_tasks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks_authorized_no_tasks(self):
        """Test getting tasks by authorized user with no tasks"""
        url = reverse("get_tasks")
        response = self.client.get(url, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_tasks_authorized_with_tasks(self):
        """Test getting tasks by authorized user with tasks"""
        # create test tasks
        Task.objects.create(priority=1, text="test task 1", user=self.user)
        Task.objects.create(priority=2, text="test task 2", user=self.user)

        tasks = Task.objects.filter(user=self.user)
        task_serializer = TaskSerializer(tasks, many=True)
        url = reverse("get_tasks")

        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task_serializer.data, response.data)

    def test_get_tasks_authorized_with_tasks(self):
        """Test getting OWN tasks by authorized user with tasks"""
        # create test task for user
        Task.objects.create(priority=1, text="test task 1", user=self.user)
        # create task for another user
        Task.objects.create(priority=2, text="test task 1", user=self.user_2)

        tasks = Task.objects.filter(user=self.user)
        task_serializer = TaskSerializer(tasks, many=True)
        url = reverse("get_tasks")

        response = self.client.get(url, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task_serializer.data, response.data)

    def test_POST_create_task_unauthorized(self):
        """Test POST request to create task by unauthorized user"""

        url = reverse("get_tasks")
        payload = {
            "priority": 1,
            "text": "test task 1",
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_POST_create_task_authorized_invalid(self):
        """Test POST request to create a task (invalid data passed) by authorized user"""

        url = reverse("get_tasks")
        payload = {
            "priority": True,  # incorrect input
            "text": "test task 1",
        }

        response = self.client.post(url, payload, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POST_create_task_authorized_valid(self):
        """Test POST request to create a task (valid data passed) by authorized user"""

        url = reverse("get_tasks")
        payload = {
            "priority": 1,
            "text": "test task 1",
        }
        response = self.client.post(url, payload, **self.headers)

        tasks = Task.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(payload["text"], tasks[0].text)


class TestTaskDetailAPI(TestCase):
    """Test TaskDetailAPI that updates and deletes tasks"""

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.client = APIClient()

        cls.user_1 = User.objects.create_user(
            email="test1@example.com", username="testuser1", password="testpassword"
        )
        cls.task_1 = Task.objects.create(
            priority=1, text="test task 1", user=cls.user_1
        )

        cls.user_2 = User.objects.create_user(
            email="test2@example.com", username="testuser2"
        )
        cls.task_2 = Task.objects.create(
            priority=1, text="test task 2", user=cls.user_2
        )
        access_token = cls.client.post(
            reverse("jwt-create"),
            data={"username": "testuser1", "password": "testpassword"},
        ).data["access"]
        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    def test_DELETE_valid(self):
        """Test that task gets deleted successfully"""

        url = reverse("change_tasks", args=[self.task_1.task_id])
        response = self.client.delete(url, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Task.objects.filter(user=self.user_1)), 0)

    def test_DELETE_unauthorized(self):
        """Test trying to delete a task by unauthorized user"""
        url = reverse("change_tasks", args=[self.task_1.task_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DELETE_other_user(self):
        """Test trying to delete a task of the another user"""

        url = reverse("change_tasks", args=[self.task_2.task_id])
        response = self.client.delete(url, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(Task.objects.filter(user=self.user_2)), 1)

    def test_PATCH_update_multiple_valid(self):
        """Test updating multiple fields at once"""
        payload = {"priority": 99, "text": "updated text"}
        url = reverse("change_tasks", args=[self.task_1.task_id])

        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Task has been updated")
        self.assertEqual(Task.objects.filter(user=self.user_1)[0].text, payload["text"])
        self.assertEqual(
            Task.objects.filter(user=self.user_1)[0].priority, payload["priority"]
        )

    def test_PATCH_update_multiple_invalid(self):
        """Test updating multiple fields at once with invalid data"""
        payload = {"priority": False, "text": "updated text"}  # invalid input
        url = reverse("change_tasks", args=[self.task_1.task_id])
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_PATCH_update_unauthorized(self):
        """Test attempt to update task by unauthorized user"""
        payload = {"text": "update by unathorized"}
        url = reverse("change_tasks", args=[self.task_1.task_id])
        response = self.client.patch(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_PATCH_update_other_user(self):
        """Test trying to update a task of the another user"""
        payload = {"text": "update by another user"}
        url = reverse("change_tasks", args=[self.task_2.task_id])
        response = self.client.patch(url, data=payload, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateTaskPriorityAPI(TestCase):
    """Test updating ordering of multiple tasks"""

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.client = APIClient()

        cls.user_1 = User.objects.create_user(
            email="test1@example.com", username="testuser1", password="testpassword"
        )
        # create 2 tasks by the first user
        cls.task_1 = Task.objects.create(
            priority=1, text="test task 1", user=cls.user_1
        )
        cls.task_2 = Task.objects.create(
            priority=2, text="test task 2", user=cls.user_1
        )
        # create 2 tasks by the second user
        cls.user_2 = User.objects.create_user(
            email="test2@example.com", username="testuser2"
        )
        cls.task_3 = Task.objects.create(
            priority=1, text="test task 3", user=cls.user_2
        )
        cls.task_4 = Task.objects.create(
            priority=2, text="test task 4", user=cls.user_2
        )
        access_token = cls.client.post(
            reverse("jwt-create"),
            data={"username": "testuser1", "password": "testpassword"},
        ).data["access"]
        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    def test_PATCH_update_priority_valid(self):
        """Test updating priorities succeeds"""

        payload = {"update": {str(self.task_1.task_id): 2, str(self.task_2.task_id): 1}}

        # double check priorities before request
        self.assertEqual(
            Task.objects.filter(task_id=self.task_1.task_id)[0].priority, 1
        )
        self.assertEqual(
            Task.objects.filter(task_id=self.task_2.task_id)[0].priority, 2
        )

        url = reverse("update_priority")
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Tasks order has been updated")
        # check priorities again
        self.assertEqual(
            Task.objects.filter(task_id=self.task_1.task_id)[0].priority, 2
        )
        self.assertEqual(
            Task.objects.filter(task_id=self.task_2.task_id)[0].priority, 1
        )

    def test_PATCH_update_priority_unauthorized(self):
        """Test updating priorities by unauthorized user"""

        payload = {
            "update": {
                "test id": 1,
                "test id 2": 2,
            }
        }
        url = reverse("update_priority")
        response = self.client.patch(url, data=payload, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_PATCH_update_priority_invalid_task_id(self):
        """Test updating priorities with invalid task_id data"""
        payload = {"update": {"invalid": 1}}  # invalid data
        url = reverse("update_priority")
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertIn("task_id is not a valid uuid field", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_PATCH_update_priority_invalid_priority_str(self):
        """Test updating priorities with invalid priority data - string"""
        payload = {"update": {str(self.task_1.task_id): True}}  # invalid priority data
        url = reverse("update_priority")
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertIn("priority is not a valid integer", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_PATCH_update_priority_invalid_priority_negative(self):
        """Test updating priorities with invalid priority data - negative num"""
        payload = {"update": {str(self.task_1.task_id): -5}}  # invalid priority data
        url = reverse("update_priority")
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertIn("priority is not a valid integer", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_PATCH_update_priority_other_users(self):
        """Test updating priorities other user's tasks"""

        payload = {
            "update": {
                str(self.task_3.task_id): 2,  # another user's task
                str(self.task_2.task_id): 1,
            }
        }

        url = reverse("update_priority")
        response = self.client.patch(
            url, data=payload, content_type="application/json", **self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "You cannot modify other users' tasks")
