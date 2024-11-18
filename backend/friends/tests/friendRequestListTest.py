from rest_framework import status
from rest_framework.test import APITestCase
from friends.models import Friend  # Import your Friend model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.urls import reverse  # Import reverse for URL resolution

User = get_user_model()  # Get the user model

class FriendRequestListViewTest(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username="user1", password="password", email="user1@test.com"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password", email="user2@test.com"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="password", email="user3@test.com"
        )

        # Create friend requests
        Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.PENDING,
        )
        Friend.objects.create(
            user1=self.user2,
            user2=self.user3,
            requester=self.user2,
            status=Friend.PENDING,
        )

        # Create the client instance
        self.client = self.client

    def test_friend_request_list_sent(self):
        """
        Test filtering by sent friend requests with pagination.
        """
        self.client.force_authenticate(user=self.user1)
        url = reverse("friend-request")
        response = self.client.get(url, {"type": "sent", "page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)  # Only 1 sent request
        self.assertEqual(response.data["results"][0]["other_user"]["username"], "user2")

    def test_friend_request_list_received(self):
        """
        Test filtering by received friend requests with pagination.
        """
        self.client.force_authenticate(user=self.user2)
        url = reverse("friend-request")
        response = self.client.get(url, {"type": "received", "page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)  # Only 1 received request
        self.assertEqual(response.data["results"][0]["other_user"]["username"], "user1")

    def test_friend_request_list_no_filter(self):
        """
        Test no filter with pagination.
        """
        self.client.force_authenticate(user=self.user2)
        url = reverse("friend-request")
        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        # one sent one received
        self.assertEqual(len(response.data["results"]), 2)  # Sent and received requests

    def test_unauthorized_access(self):
        """
        Test that unauthorized users cannot access the friend request list.
        """
        url = reverse("friend-request")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
