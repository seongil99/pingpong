from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from tournament.models import Tournament, TournamentMatchParticipants, TournamentGame
from pingpong_history.models import PingPongHistory
from tournament.utils import create_tournament, start_round, finish_game, check_and_advance_round, create_pingpong_round

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
        history = PingPongHistory.objects.get(id=g1.game_id.id)
        create_pingpong_round(history, 3, timezone.now(), timezone.now(), 1, 0)
        create_pingpong_round(history, 1, timezone.now(), timezone.now(), 3, 1)
        create_pingpong_round(history, 3, timezone.now(), timezone.now(), 3, 1)
        history.refresh_from_db()

        # round2 시작 및 종료 (user4 승리)
        # check_and_advance_round 호출로 round2가 시작되었다고 가정
        # (utils에서 check_and_advance_round가 start_round(2)를 호출)
        g2 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=2).first()
        finish_game(g2.game_id.id, 2, 3)
        self.tournament.refresh_from_db()
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()
        history = PingPongHistory.objects.get(id=g2.game_id.id)
        create_pingpong_round(history, 2, timezone.now(), timezone.now(), 2, 3)
        create_pingpong_round(history, 3, timezone.now(), timezone.now(), 2, 3)
        history.refresh_from_db()

        # round3 시작 및 종료 (user1 최종 승리)
        g3 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=3).first()
        finish_game(g3.game_id.id, 3, 2)
        self.tournament.refresh_from_db()
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()
        history = PingPongHistory.objects.get(id=g3.game_id.id)
        create_pingpong_round(history, 3, timezone.now(), timezone.now(), 3, 2)
        create_pingpong_round(history, 2, timezone.now(), timezone.now(), 3, 2)
        create_pingpong_round(history, 3, timezone.now(), timezone.now(), 3, 2)
        history.refresh_from_db()

        self.url = reverse('tournament-detail', args=[self.tournament.tournament_id])

    def test_tournament_detail_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # 최상위 키 검사
        self.assertIn('tournament_id', data)
        self.assertIn('status', data)
        self.assertIn('created_at', data)
        self.assertIn('current_round', data)
        self.assertIn('participants', data)
        self.assertIn('sessions', data)

        self.assertEqual(data['tournament_id'], 1)
        self.assertEqual(data['status'], 'finished')
        self.assertEqual(data['current_round'], 3)

        # participants 내부 키 검사
        participants = data['participants']
        self.assertIn('tournament', participants)
        self.assertIn('user1', participants)
        self.assertIn('user2', participants)
        self.assertIn('user3', participants)
        self.assertIn('user4', participants)

        self.assertEqual(participants['tournament'], 1)
        self.assertEqual(participants['user1'], 1)
        self.assertEqual(participants['user2'], 2)
        self.assertEqual(participants['user3'], 3)
        self.assertEqual(participants['user4'], 4)

        # sessions 검사
        sessions = data['sessions']
        self.assertTrue(isinstance(sessions, list))
        self.assertEqual(len(sessions), 3)  # 3개의 세션

        # 첫번째 세션 검사
        first_session = sessions[0]
        self.assertIn('id', first_session)
        self.assertIn('started_at', first_session)
        self.assertIn('ended_at', first_session)
        self.assertIn('user1_score', first_session)
        self.assertIn('user2_score', first_session)
        self.assertIn('gamemode', first_session)
        self.assertIn('longest_rally', first_session)
        self.assertIn('average_rally', first_session)
        self.assertIn('user1', first_session)
        self.assertIn('user2', first_session)
        self.assertIn('winner', first_session)
        self.assertIn('rounds', first_session)

        self.assertEqual(first_session['id'], 1)
        self.assertEqual(first_session['user1_score'], 3)
        self.assertEqual(first_session['user2_score'], 1)
        self.assertEqual(first_session['gamemode'], 'PVP')
        self.assertEqual(first_session['user1'], 1)
        self.assertEqual(first_session['user2'], 2)
        self.assertEqual(first_session['winner'], 1)

        # rounds 검사
        rounds = first_session['rounds']
        self.assertTrue(isinstance(rounds, list))
        self.assertEqual(len(rounds), 3)

        # 첫번째 round 확인
        first_round = rounds[0]
        self.assertIn('user1_score', first_round)
        self.assertIn('user2_score', first_round)
        self.assertIn('rally', first_round)
        self.assertIn('start', first_round)
        self.assertIn('end', first_round)

        self.assertEqual(first_round['user1_score'], 1)
        self.assertEqual(first_round['user2_score'], 0)
        self.assertEqual(first_round['rally'], 3)
