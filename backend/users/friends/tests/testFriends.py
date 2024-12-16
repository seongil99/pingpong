from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Friend
from ..serializers import FriendSerializer
from django.urls import reverse

User = get_user_model()

import logging

logger = logging.getLogger("django")


class FriendsViewSetTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", password="password1", email="a"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password2", email="b"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="password3", email="c"
        )

        # Create a friend relationship for user1
        self.friend1 = Friend.objects.create(user=self.user1, friend_user=self.user2)

        # Authentication setup
        self.url = reverse("friends-list")  # Adjust URL as needed
        self.client.force_authenticate(user=self.user1)

    def test_list_friends(self):
        """
        Test that the endpoint returns a list of friends for the authenticated user.
        """
        response = self.client.get(self.url)  # Adjust endpoint as needed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the returned data matches the user's friends
        expected_data = FriendSerializer([self.friend1], many=True).data
        self.assertEqual(response.json()["results"], expected_data)

    def test_create_friend(self):
        """
        Test that the endpoint allows an authenticated user to add a new friend.
        """
        response = self.client.post(self.url, {"friend_user": self.user3.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the friend relationship was created
        self.assertTrue(
            Friend.objects.filter(user=self.user1, friend_user=self.user3).exists()
        )

        # Verify the response data
        created_friend = Friend.objects.get(user=self.user1, friend_user=self.user3)
        expected_data = FriendSerializer(created_friend).data
        self.assertEqual(response.json(), expected_data)

    def test_create_friend_invalid_user(self):
        """
        Test that creating a friend fails if the provided friend_user does not exist.
        """
        response = self.client.post(
            self.url, {"friend_user": 9999}
        )  # Non-existent user ID
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "friend_user", response.json()
        )  # Ensure the error points to the correct field

    def test_list_friends_unauthenticated(self):
        """
        Test that unauthenticated users cannot access the friends list.
        """
        self.client.logout()  # Logout the user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_friend_unauthenticated(self):
        """
        Test that unauthenticated users cannot create a friend.
        """
        self.client.logout()
        response = self.client.post(self.url, {"friend_user": self.user3.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_friend_self(self):
        """
        Test that a user cannot add themselves as a friend.
        """
        response = self.client.post(self.url, {"friend_user": self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.json())

    def test_create_friend_duplicate(self):
        """
        Test that a user cannot add the same friend twice.
        """
        response = self.client.post(self.url, {"friend_user": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.json())
