from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone

from tournament.models import Tournament, TournamentMatchParticipants
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


class EventViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123', username='PlayerOne')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123', username='PlayerTwo')
        self.user3 = User.objects.create_user(email='user3@example.com', password='password123', username='PlayerThree')
        self.user4 = User.objects.create_user(email='user4@example.com', password='password123', username='PlayerFour')

        # 인증 토큰 설정
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # 단일 match 생성
        self.match_history = PingPongHistory.objects.create(
            user1=self.user1,
            user2=self.user2,
            user1_score=3,
            user2_score=1,
            winner=self.user1,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now()
        )

        # 토너먼트 생성 및 match들 생성
        self.tournament = Tournament.objects.create(status='pending', current_round=0)
        # 토너먼트 참가자 연결
        TournamentMatchParticipants.objects.create(
            tournament=self.tournament,
            user1=self.user1,
            user2=self.user2,
            user3=self.user3,
            user4=self.user4
        )

        # 토너먼트용 match들 (여기서는 그냥 2개 정도 만들고 하나만 winner 설정)
        self.t_history1 = PingPongHistory.objects.create(
            user1=self.user1,
            user2=self.user2,
            user1_score=21,
            user2_score=19,
            winner=self.user1,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now(),
            tournament_id=self.tournament
        )
        self.t_history2 = PingPongHistory.objects.create(
            user1=self.user3,
            user2=self.user4,
            user1_score=2,
            user2_score=3,
            winner=self.user4,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now(),
            tournament_id=self.tournament
        )

    def test_get_match_event(self):
        # 단일 match 조회
        url = reverse('event-detail', args=["match", self.match_history.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        print(data)

        self.assertEqual(data["eventType"], "match")
        self.assertEqual(data["eventId"], self.match_history.id)
        self.assertEqual(len(data["matches"]), 1)
        match_data = data["matches"][0]
        self.assertEqual(match_data["matchId"], self.match_history.id)
        # 플레이어 정보 확인
        players = match_data["players"]
        self.assertEqual(len(players), 2)
        # 승자/패자 체크
        p1 = players[0]
        p2 = players[1]
        # user1이 winner
        self.assertEqual(p1["name"], "PlayerOne")
        self.assertEqual(p1["status"], "winner")
        self.assertEqual(p2["name"], "PlayerTwo")
        self.assertEqual(p2["status"], "loser")

    def test_get_tournament_event(self):
        # 토너먼트 조회
        url = reverse('event-detail', args=["tournament", self.tournament.tournament_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        print(data)

        self.assertEqual(data["eventType"], "tournament")
        self.assertEqual(data["eventId"], self.tournament.tournament_id)
        # t_history1, t_history2 총 2개 매치
        self.assertEqual(len(data["matches"]), 2)

        # 첫번째 match는 user1 vs user2
        m1 = data["matches"][0]
        self.assertIn("players", m1)
        p1 = m1["players"][0]
        p2 = m1["players"][1]
        self.assertEqual(p1["name"], "PlayerOne")
        self.assertEqual(p1["status"], "winner")
        self.assertEqual(p2["name"], "PlayerTwo")
        self.assertEqual(p2["status"], "loser")

        # 두번째 match는 user3 vs user4
        m2 = data["matches"][1]
        p3 = m2["players"][0]
        p4 = m2["players"][1]
        self.assertEqual(p3["name"], "PlayerThree")
        self.assertEqual(p3["status"], "loser")
        self.assertEqual(p4["name"], "PlayerFour")
        self.assertEqual(p4["status"], "winner")

    def test_get_nonexistent_match(self):
        url = reverse('event-detail', args=["match", 9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_tournament(self):
        url = reverse('event-detail', args=["tournament", 9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_event_type(self):
        url = reverse('event-detail', args=["invalidtype", self.match_history.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        self.client.credentials()  # 인증 제거
        url = reverse('event-detail', args=["match", self.match_history.id])
        response = self.client.get(url)
        # 인증 필요하다면 401 반환 예상
        # 만약 인증이 필요 없도록 설정했다면 이 부분 조정 필요
        # 여기서는 인증 필요하다고 가정
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
