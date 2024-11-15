# tests.py or in a test module in your app
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .decorators import spa_login_required
from django.http import JsonResponse


class DecoratorTestCase(TestCase):
    
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()

    def test_spa_login_required_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Make a request to a view protected by the spa_login_required decorator
        response = self.client.get(reverse('some_api_view'))  # Adjust URL as needed

        # Assert the response is as expected
        self.assertEqual(response.status_code, 200)  # Assuming the user is authenticated

    def test_spa_login_required_unauthenticated(self):
        # Ensure the user is logged out
        self.client.logout()

        # Make a request to a view protected by the spa_login_required decorator
        response = self.client.get(reverse('some_api_view'))  # Adjust URL as needed

        # Assert that the response is 401 Unauthorized
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication required"})

    def test_spa_login_required_no_user(self):
        # Make a request without logging in (user is anonymous)
        response = self.client.get(reverse('some_api_view'))  # Adjust URL as needed

        # Assert that the response is 401 Unauthorized
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication required"})
