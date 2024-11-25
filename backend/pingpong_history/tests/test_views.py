from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from users.models import User
from pingpong_history.models import PingPongHistory
from rest_framework_simplejwt.tokens import RefreshToken


class PingPongHistoryAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

        # 인증을 위한 토큰 생성
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # 샘플 게임 기록 생성
        PingPongHistory.objects.create(
            user1=self.user1,
            user2=self.user2,
            user1_score=21,
            user2_score=19,
            winner=self.user1,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now()
        )

    def test_get_all_pingpong_history(self):
        url = reverse('pingpong-history-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_pingpong_history_by_user(self):
        url = reverse('pingpong-history-by-user', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_pingpong_history_by_id(self):
        game = PingPongHistory.objects.first()
        url = reverse('pingpong-history-by-id', args=[game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], game.id)

    def test_get_nonexistent_pingpong_history_by_id(self):
        url = reverse('pingpong-history-by-id', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.credentials()  # 인증 제거
        url = reverse('pingpong-history-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
