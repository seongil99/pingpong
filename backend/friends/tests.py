from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Friend
from .error import FriendError
from .detail import FriendDetail
from common.error import Error

User = get_user_model()

class FriendRequestTests(APITestCase):

    def setUp(self):
        # Create two users for testing, now including email
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",  # Adding email
            password="password123",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",  # Adding email
            password="password123",
        )
        self.client.force_authenticate(user=self.user1)

    def test_send_friend_request(self):
        """Test sending a valid friend request."""
        url = reverse("friend-request")  # Assuming FriendsView's URL is named 'friends'
        data = {"target_user": self.user2.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user1"], self.user1.id)
        self.assertEqual(response.data["user2"], self.user2.id)
        self.assertEqual(response.data["status"], Friend.PENDING)

    def test_send_friend_request_invalid_user(self):
        """Test sending a friend request to an invalid user."""
        url = reverse("friend-request")
        data = {"target_user": 9999}  # Non-existent user ID

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], Error.USER_NOT_FOUND.value)

    def test_duplicate_friend_request(self):
        """Test sending a duplicate friend request."""
        Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.PENDING,
        )

        url = reverse("friend-request")
        data = {"target_user": self.user2.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], FriendError.REQUEST_ALREADY_SENT.value)

    def test_send_friend_request_already_friends(self):
        """Test sending a friend request to a user that is already a friend."""
        Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.ACCEPTED,
        )

        url = reverse("friend-request")
        data = {"target_user": self.user2.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], FriendError.ALREADY_FRIENDS.value)


class FriendRequestActionTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",  # Adding email
            password="password123",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",  # Adding email
            password="password123",
        )
        self.client.force_authenticate(user=self.user1)

    def test_accept_friend_request(self):
        """Test accepting a friend request."""
        friend_request = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user2,
            status=Friend.PENDING,
        )

        url = reverse("friend-request-action", kwargs={"id": friend_request.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], Friend.ACCEPTED)

    def test_accept_non_pending_friend_request(self):
        """Test accepting a friend request that isn't in 'PENDING' state."""
        friend_request = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user2,
            status=Friend.ACCEPTED,
        )

        url = reverse("friend-request-action", kwargs={"id": friend_request.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], FriendError.INVALID_REQUEST.value)

    def test_accept_non_existent_friend_request(self):
        """Test accepting a non-existent friend request."""
        url = reverse("friend-request-action", kwargs={"id": 9999})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], FriendError.REQ_NOT_EXIST.value)

    def test_reject_friend_request(self):
        """Test rejecting a friend request."""
        friend_request = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user1,
            status=Friend.PENDING,
        )

        url = reverse("friend-request-action", kwargs={"id": friend_request.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], FriendDetail.REQUEST_REJECTED.value)

    def test_reject_non_pending_friend_request(self):
        """Test rejecting a friend request that isn't in 'PENDING' state."""
        friend_request = Friend.objects.create(
            user1=self.user1,
            user2=self.user2,
            requester=self.user2,
            status=Friend.ACCEPTED,
        )

        url = reverse("friend-request-action", kwargs={"id": friend_request.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], FriendError.INVALID_REQUEST.value)

    def test_reject_non_existent_friend_request(self):
        """Test rejecting a non-existent friend request."""
        url = reverse("friend-request-action", kwargs={"id": 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], FriendError.DOES_NOT_EXIST.value)
