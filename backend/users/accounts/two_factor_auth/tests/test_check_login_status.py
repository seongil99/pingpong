from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class CheckLoginStatusViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            "check-login-status"
        )  # Replace with your actual endpoint URL.

    def test_user_logged_in_status(self):
        # Simulate a logged-in user by setting session data
        session = self.client.session
        session["userId"] = 1  # Mock user ID
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "logged in"})

    def test_user_logged_out_status(self):
        # No session data, simulates logged-out user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"status": "logged out"})
