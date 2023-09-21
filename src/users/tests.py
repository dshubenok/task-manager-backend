import unittest
from django.test import Client
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):
    def test_register_user(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("users-register")
        data = {"username": "admin", "password": "admin"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "admin")
