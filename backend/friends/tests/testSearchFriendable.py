from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from friends.models import Friend
from django.urls import reverse

User = get_user_model()


class SearchFriendableViewTest(APITestCase):
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
        self.user4 = User.objects.create_user(
            username="user4", password="password", email="user4@test.com"
        )

        # Create friend relationships with different statuses
        Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.ACCEPTED,
        )  # user1 and user2 are friends (accepted)

        Friend.objects.create(
            user1=self.user2,
            user2=self.user3,
            requester=self.user2,
            status=Friend.PENDING,
        )  # user2 and user3 have a pending request

        Friend.objects.create(
            user1=self.user3,
            user2=self.user4,
            requester=self.user3,
            status=Friend.BLOCKED,
        )  # user3 has blocked user4

        # URL for the SearchFriendableView
        self.url = reverse("search-friendable")  # Update with your URL name

    def test_search_friendable_users_authenticated(self):
        """
        Test that authenticated users can search for users who can be sent friend requests.
        """
        self.client.force_authenticate(user=self.user1)

        # Fetch friendable users (users who are not in the friends table, pending, or blocked)
        response = self.client.get(self.url, {"search": ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Only user3 and user4 should be returned (user1 is friends with user2)
        usernames = [user["username"] for user in response.data["results"]]
        self.assertIn("user3", usernames)
        self.assertIn("user4", usernames)

    def test_search_friendable_users_with_pending(self):
        """
        Test that pending and blocked users are excluded from search results.
        """
        self.client.force_authenticate(user=self.user2)

        # Search for friendable users, user3 should not be included because they are in pending status with user2
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Only user4 should be returned
        usernames = [user["username"] for user in response.data["results"]]
        self.assertIn("user4", usernames)
        
    def test_search_friendable_users_with_blocked(self):
        """
        Test that pending and blocked users are excluded from search results.
        """
        self.client.force_authenticate(user=self.user3)

        # Search for friendable users, user3 should not be included because they are in pending status with user2
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Only user1 and user4 should be returned, not user3
        usernames = [user["username"] for user in response.data["results"]]
        self.assertIn("user1", usernames)
        
    def test_search_friendable_users_with_blocked_reverse(self):
        """
        Test that pending and blocked users are excluded from search results.
        """
        self.client.force_authenticate(user=self.user4)

        # Search for friendable users, user3 should not be included because they are in pending status with user2
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Only user1 and user4 should be returned, not user3
        usernames = [user["username"] for user in response.data["results"]]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)
        self.assertNotIn(
            "user3", usernames
        )  # user3 should not be included due to pending status


    def test_search_friendable_users_with_search_param(self):
        """
        Test that the search parameter filters users based on email or username.
        """
        self.client.force_authenticate(user=self.user1)

        # Search for user3 by email
        response = self.client.get(self.url, {"search": "user3@test.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Only user3 should be returned (pending status)
        self.assertEqual(response.data["results"][0]["username"], "user3")

        # Search for blocked user4 by username (user4 should be returned because blocking doesn't exclude)
        response = self.client.get(self.url, {"search": "user4"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Only user4 should be returned
        self.assertEqual(response.data["results"][0]["username"], "user4")

    def test_search_friendable_users_unauthenticated(self):
        """
        Test that unauthenticated users cannot access the search endpoint.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_friendable_no_results(self):
        """
        Test that when no users match the search term, the result is empty.
        """
        self.client.force_authenticate(user=self.user1)

        # Search for a user that doesn't exist
        response = self.client.get(self.url, {"search": "nonexistentuser"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)  # No users should be returned

    def test_search_friendable_users_no_search_param(self):
        """
        Test that users can be returned even if no search parameter is provided.
        """
        self.client.force_authenticate(user=self.user1)

        # Get friendable users without any search parameter
        response = self.client.get(self.url, {"search": ""})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Only user3 and user4 should be returned (user1 is friends with user2)
        self.assertEqual(
            sorted([user["username"] for user in response.data["results"]]),
            sorted(["user3", "user4"]),
        )
