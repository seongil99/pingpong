from rest_framework.decorators import api_view
from rest_framework.response import Response
from .decorators import spa_login_required

@api_view(['GET'])
@spa_login_required
def spaLoginRequiredView(request):
    return Response({'message': 'Success'}, status = 200)

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class LoginRequiredViewTestCase(TestCase):
    
    def setUp(self):
        # Set up a test user
        self.user = User.objects.create_user(username='testuser', password='password', email='test@test.com')
        self.factory = APIRequestFactory()

    def test_spa_login_required_authenticated(self):
        # Create a GET request using the APIRequestFactory
        request = self.factory.get(reverse('login_required'))
        
        # Force authentication on the request
        force_authenticate(request, user=self.user)

        # Pass the request to the view
        view = spaLoginRequiredView
        response = view(request)

        # Assert the response is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Success"})

    def test_spa_login_required_unauthenticated(self):
        # Create a GET request using the APIRequestFactory (without authentication)
        request = self.factory.get(reverse('login_required'))

        # Pass the request to the view without authentication
        view = spaLoginRequiredView
        response = view(request)

        # Assert that the response is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication required"})