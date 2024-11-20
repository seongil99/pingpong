from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Friend
from ..error import FriendError
from ..detail import FriendDetail
from common.error import Error

User = get_user_model()


class FriendListViewTest(APITestCase):

    def setUp(self):
        # Create test users with email addresses
        self.user1 = User.objects.create_user(
            username="user1", password="password123", email="user1@example.com"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123", email="user2@example.com"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="password123", email="user3@example.com"
        )

        # Create friends with accepted status (user1 is the requester)
        self.friendship1 = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.ACCEPTED,
        )
        self.friendship2 = Friend.objects.create(
            user1=self.user1,
            user2=self.user3,
            requester=self.user3,
            status=Friend.ACCEPTED,
        )

        # URL for the API endpoint
        self.url = reverse("friends-list")  # Assuming the URL is named 'friend-list'

    def test_get_friends_with_accepted_status_user1(self):
        # Force authenticate the client as user1
        self.client.force_authenticate(user=self.user1)

        # Make a GET request
        response = self.client.get(self.url)
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the correct friends are returned
        friends_data = response.data["results"]
        self.assertEqual(len(friends_data), 2)  # Should return 2 friends
        friend_usernames = [friend["other_user"]["username"] for friend in friends_data]
        self.assertIn("user2", friend_usernames)
        self.assertIn("user3", friend_usernames)

    def test_get_friends_with_accepted_status_user2(self):
        # Force authenticate the client as user1
        self.client.force_authenticate(user=self.user2)

        # Make a GET request
        response = self.client.get(self.url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the correct friends are returned
        friends_data = response.data["results"]
        self.assertEqual(len(friends_data), 1)  # Should return 2 friends
        friend_usernames = [friend["other_user"]["username"] for friend in friends_data]
        self.assertIn("user1", friend_usernames)

    def test_get_friends_with_accepted_status_user3(self):
        # Force authenticate the client as user1
        self.client.force_authenticate(user=self.user3)

        # Make a GET request
        response = self.client.get(self.url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the correct friends are returned
        friends_data = response.data["results"]
        self.assertEqual(len(friends_data), 1)  # Should return 2 friends
        friend_usernames = [friend["other_user"]["username"] for friend in friends_data]
        self.assertIn("user1", friend_usernames)

    def test_requester_field_is_set_correctly(self):
        # Check that the 'requester' field is correctly set when creating a friend relationship
        self.assertEqual(self.friendship1.requester, self.user1)
        self.assertEqual(self.friendship2.requester, self.user3)

    def test_get_friends_with_no_accepted_friends(self):
        # Create a new user who has no accepted friends
        user4 = User.objects.create_user(
            username="user4", password="password123", email="user4@example.com"
        )

        # Force authenticate the client as user4
        self.client.force_authenticate(user=user4)

        # Make a GET request
        response = self.client.get(self.url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that no friends are returned
        friends_data = response.data["results"]
        self.assertEqual(len(friends_data), 0)  # No friends should be returned


class FriendsViewSetTestCase(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", password="password", email="user1@test.com"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password", email="user2@test.com"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="password", email="user3@test.com"
        )
        self.user4 = User.objects.create_user(
            username="user4", password="password", email="user4@test.com"
        )

        # Create a friendship between user1 and user2
        self.friendship = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.ACCEPTED,
        )

        # Create a friendship between user1 and user3
        self.friendship2 = Friend.objects.create(
            user1=self.user1,
            user2=self.user3,
            requester=self.user1,
            status=Friend.ACCEPTED,
        )

        self.friendship3 = Friend.objects.create(
            user1=self.user1,
            user2=self.user4,
            requester=self.user1,
            status=Friend.BLOCKED,
        )

        # Authentication setup
        self.client.force_authenticate(user=self.user1)

    def test_list_friends(self):
        """Test retrieving the list of friends."""
        url = reverse("friends-list")  # Ensure this URL matches your path
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Should return 2 friends (user2, user3)
        self.assertEqual(response.data["results"][0]["other_user"]["username"], "user2")
        self.assertEqual(response.data["results"][1]["other_user"]["username"], "user3")

    def test_retrieve_friend(self):
        """Test retrieving a specific friend."""
        url = reverse("friends-detail", kwargs={"pk": self.friendship.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["other_user"]["username"], "user2")
        self.assertEqual(response.data["status"], Friend.ACCEPTED)

    def test_unfriend(self):
        """Test unfriending a user."""
        url = reverse("friends-detail", kwargs={"pk": self.friendship.id})
        response = self.client.delete(url)

        # Ensure the friendship status is updated to 'Blocked' (assuming block action)
        self.assertNotIn(self.friendship, Friend.objects.all())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unfriend_non_existent(self):
        """Test unfriending a non-existent friendship."""
        url = reverse("friends-detail", kwargs={"pk": 9999})  # Non-existent ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
