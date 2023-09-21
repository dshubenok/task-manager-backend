from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from tasks.models import Task
from users.models import User


class TaskAuthorizedTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        data = {"username": "admin", "password": "admin"}
        self.client.post(reverse("users-register"), data, format="json")

    def test_create_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"title": "Test task"}
        response = self.client.post("/api/v1/tasks/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Test task")

    def test_update_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"title": "Title1"}
        response = self.client.post("/api/v1/tasks/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        data = {"title": "Title2"}
        response = self.client.patch("/api/v1/tasks/1/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, "Title2")

    def test_delete_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"title": "Test title"}
        response = self.client.post("/api/v1/tasks/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        response = self.client.delete("/api/v1/tasks/1/", format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_assignee_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"username": "second_user", "password": "123"}
        self.client.post(reverse("users-register"), data, format="json")
        self.assertEqual(User.objects.count(), 2)

        data = {"title": "Test title"}
        response = self.client.post("/api/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().assignee, None)

    def test_complete_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"title": "Test title"}
        response = self.client.post("/api/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().is_completed, False)

        response = self.client.patch("/api/v1/tasks/1/complete/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().is_completed, True)

    def test_comment_task(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)

        data = {"title": "Test title"}
        response = self.client.post("/api/v1/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().is_completed, False)

        data = {"author": 1, "body": "123"}
        response = self.client.post("/api/v1/tasks/1/comment/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.all()[0].comments.count(), 1)
