from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from tournament.models import Tournament, TournamentMatchParticipants, TournamentGame
from pingpong_history.models import PingPongHistory
from tournament.utils import create_tournament, start_round, finish_game, check_and_advance_round

User = get_user_model()


class TournamentEventViewTest(TestCase):
    def setUp(self):
        # 유저 및 토너먼트 생성
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='playerOne', email='one@example.com', password='pass')
        self.user2 = User.objects.create_user(username='playerTwo', email='two@example.com', password='pass')
        self.user3 = User.objects.create_user(username='playerThree', email='three@example.com', password='pass')
        self.user4 = User.objects.create_user(username='playerFour', email='four@example.com', password='pass')
        self.client.force_authenticate(user=self.user1)

        self.tournament = create_tournament(self.user1, self.user2, self.user3, self.user4)

        # round1 시작 및 종료 (user1 승리)
        start_round(self.tournament, 1)
        self.tournament.refresh_from_db()
        g1 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=1).first()
        finish_game(g1.game_id.id, 3, 1)
        self.tournament.refresh_from_db()
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()

        # round2 시작 및 종료 (user4 승리)
        # check_and_advance_round 호출로 round2가 시작되었다고 가정
        # (utils에서 check_and_advance_round가 start_round(2)를 호출)
        g2 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=2).first()
        finish_game(g2.game_id.id, 2, 3)
        self.tournament.refresh_from_db()
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()

        # round3 시작 및 종료 (user1 최종 승리)
        g3 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=3).first()
        finish_game(g3.game_id.id, 3, 2)
        self.tournament.refresh_from_db()
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()

        self.url = reverse('tournament-event', args=[self.tournament.tournament_id])

    def test_tournament_event_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 기본 필드 확인
        self.assertEqual(data["eventId"], self.tournament.tournament_id)
        self.assertEqual(data["eventType"], "tournament")
        self.assertIn("matches", data)
        self.assertEqual(len(data["matches"]), 3)  # round1, round2, round3 총 3경기

        # round1 match 확인
        # round1: user1 vs user2
        m1 = data["matches"][0]
        self.assertIn("matchId", m1)
        self.assertIn("round", m1)
        self.assertIn("startTime", m1)
        self.assertIn("endTime", m1)
        self.assertIn("players", m1)
        self.assertEqual(len(m1["players"]), 2)

        p1 = m1["players"][0]
        p2 = m1["players"][1]
        # user1 승리 로직이므로 user1 status: 'winner', user2: 'loser'
        # user1.name == 'playerOne', user2.name == 'playerTwo'
        self.assertEqual(p1["name"], "playerOne")
        self.assertEqual(p1["status"], "winner")
        self.assertEqual(p2["name"], "playerTwo")
        self.assertEqual(p2["status"], "loser")

        # round2 match 확인
        # round2: user3 vs user4
        m2 = data["matches"][1]
        self.assertEqual(len(m2["players"]), 2)
        p3 = m2["players"][0]
        p4 = m2["players"][1]
        # user4 승리 가정
        self.assertEqual(p3["name"], "playerThree")
        self.assertEqual(p3.get("status", ""), "loser")  # 패자는 명시적 loser or 빈칸일 수 있음
        self.assertEqual(p4["name"], "playerFour")
        self.assertEqual(p4["status"], "winner")

        # round3 match 확인
        # round3: round_1_winner(user1) vs round_2_winner(user4)
        m3 = data["matches"][2]
        self.assertEqual(len(m3["players"]), 2)
        p_final1 = m3["players"][0]
        p_final2 = m3["players"][1]
        # 최종 user1 승
        self.assertEqual(p_final1["name"], "playerOne")
        self.assertEqual(p_final1["status"], "winner")
        self.assertEqual(p_final2["name"], "playerFour")
        self.assertEqual(p_final2["status"], "loser")