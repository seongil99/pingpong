from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from rest_framework.reverse import reverse

User = get_user_model()

class UserSearchViewTest(APITestCase):
    def setUp(self):
        # Create some test users
        self.user1 = User.objects.create_user(
            email="test1@example.com", username="testuser1", password="password123"
        )
        self.user2 = User.objects.create_user(
            email="test2@example.com", username="testuser2", password="password123"
        )
        self.user3 = User.objects.create_user(
            email="example3@example.com",
            username="user3example",
            password="password123",
        )

        # URL for search endpoint
        self.url = reverse(
            "user-search"
        )  # Assuming you've named the URL as 'user-search'
        self.client.force_authenticate(user=self.user1)

    def test_search_with_valid_query(self):
        # Force authenticate with user1
        force_authenticate(self.client, user=self.user1)

        # Search for users with "example" in their email or username
        response = self.client.get(self.url, {"q": "example"})

        # Check status code and pagination metadata
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        # Ensure pagination keys are correctly included
        self.assertGreater(
            response.data["count"], 0
        )  # Total count should be greater than 0
        self.assertTrue(
            response.data["next"] is None or isinstance(response.data["next"], str)
        )
        self.assertTrue(
            response.data["previous"] is None
            or isinstance(response.data["previous"], str)
        )

        # Check the results list matches the query
        emails = [user["email"] for user in response.data["results"]]
        self.assertIn("test2@example.com", emails)
        self.assertIn("example3@example.com", emails)

    def test_search_with_empty_query(self):
        # Force authenticate with user1
        force_authenticate(self.client, user=self.user1)

        # Search with an empty query should return no results
        response = self.client.get(self.url, {"q": ""})

        # The response should be an empty list and pagination metadata
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_search_with_no_results(self):
        # Force authenticate with user1
        force_authenticate(self.client, user=self.user1)

        # Search for a query that doesn't match any users
        response = self.client.get(self.url, {"q": "nonexistent"})

        # The response should be an empty list and pagination metadata
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_search_with_authenticated_user(self):
        # Force authenticate with user1
        force_authenticate(self.client, user=self.user1)

        # Make sure the authenticated user is excluded from the search
        response = self.client.get(self.url, {"q": "testuser", "exclude_me": "true"})

        # The response should include pagination metadata
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        # Only user2 should be returned, as user1 is excluded
        emails = [user["email"] for user in response.data["results"]]
        self.assertEqual(len(response.data["results"]), 1)  # Only user2 should match
        self.assertNotIn(self.user1.email, emails)
        self.assertIn(self.user2.email, emails)

    def test_search_with_incomplete_query(self):
        # Force authenticate with user1
        force_authenticate(self.client, user=self.user1)

        # Search with a partial query (case-insensitive)
        response = self.client.get(self.url, {"q": "test", "exclude_me": "true"})

        # The response should include user1 and user2 because "test" is part of their username/email
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        emails = [user["email"] for user in response.data["results"]]
        # no user1 because exclude_me is true
        self.assertIn(self.user2.email, emails)

    def test_unauthenticated_search(self):
        self.client.logout()
        # Test if the view enforces authentication
        response = self.client.get(self.url, {"q": "test"})

        # Should return a 401 Unauthorized error if not authenticated
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
