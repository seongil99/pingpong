from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tournament.models import Tournament, TournamentMatchParticipants
from django.contrib.auth import get_user_model

User = get_user_model()


class TournamentViewTests(APITestCase):
    def setUp(self):
        # 사용자 생성
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@test.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@test.com")
        self.user3 = User.objects.create_user(username="user3", password="password3", email="user3@test.com")
        self.user4 = User.objects.create_user(username="user4", password="password4", email="user4@test.com")
        self.client.force_authenticate(user=self.user1)

        # 토너먼트 생성
        self.tournament1 = Tournament.objects.create(
            status="ongoing", current_round=1
        )
        self.tournament2 = Tournament.objects.create(
            status="pending", current_round=0
        )

        # 토너먼트 참가자 생성
        self.participants = TournamentMatchParticipants.objects.create(
            tournament=self.tournament1,
            user1=self.user1,
            user2=self.user2,
            user3=self.user3,
            user4=self.user4,
        )

    def test_tournament_all_view(self):
        """
        Test retrieving all tournaments.
        """
        url = reverse("tournament-all")  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)  # 2 tournaments created
        self.assertEqual(response.data["results"][0]["status"], "ongoing")

    def test_tournament_by_tournament_id_view(self):
        """
        Test retrieving a tournament by its ID.
        """
        url = reverse("tournament-by-id", kwargs={"tournament_id": self.tournament1.tournament_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tournament_id"], self.tournament1.tournament_id)

    def test_tournament_by_user_id_view(self):
        """
        Test retrieving tournaments associated with a user.
        """
        url = reverse("tournament-by-user", kwargs={"user_id": self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)  # Only 1 tournament associated with the user
        self.assertEqual(response.data["results"][0]["tournament_id"], self.tournament1.tournament_id)
