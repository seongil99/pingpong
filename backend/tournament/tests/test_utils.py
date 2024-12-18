from django.test import TestCase
from django.contrib.auth import get_user_model
from tournament.utils import (
    create_tournament, start_round, finish_game, check_and_advance_round
)
from tournament.models import Tournament, TournamentMatchParticipants, TournamentGame
from pingpong_history.models import PingPongHistory

User = get_user_model()


class TournamentUtilsTest(TestCase):
    def setUp(self):
        # 4명의 유저 생성
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='pass')
        self.user4 = User.objects.create_user(username='user4', email='user4@example.com', password='pass')

        self.tournament = create_tournament(self.user1, self.user2, self.user3, self.user4)

    def test_create_tournament(self):
        self.assertEqual(self.tournament.status, 'pending')
        self.assertEqual(self.tournament.current_round, 0)
        participants = TournamentMatchParticipants.objects.get(tournament=self.tournament)
        self.assertEqual(participants.user1, self.user1)
        self.assertEqual(participants.user2, self.user2)
        self.assertEqual(participants.user3, self.user3)
        self.assertEqual(participants.user4, self.user4)

    def test_round1_and_round2_flow(self):
        # Round1 시작
        start_round(self.tournament, 1)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.current_round, 1)
        self.assertEqual(self.tournament.status, 'ongoing')

        # Round1 경기 확인
        game_round1 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=1).first()
        self.assertIsNotNone(game_round1)
        history = game_round1.game_id
        self.assertIsInstance(history, PingPongHistory)

        # Round1 경기 종료 (user1 승리 가정)
        finish_game(history.id, user1_score=3, user2_score=1)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.round_1_winner, self.user1)

        # round1 끝났으니 check_and_advance_round 호출 -> round2 시작
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()
        # round2가 시작되었는지 확인
        # start_round(2)가 호출되어야 round2 game 생성됨
        game_round2 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=2).first()
        self.assertIsNotNone(game_round2)
        self.assertEqual(self.tournament.current_round, 2)

        # round2 종료 (user4 승리 가정)
        finish_game(game_round2.game_id.id, user1_score=2, user2_score=3)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.round_2_winner, game_round2.user_2)  # user4가 승자

        # round2 끝났으니 round3로 진행
        check_and_advance_round(self.tournament)
        self.tournament.refresh_from_db()
        game_round3 = TournamentGame.objects.filter(tournament_id=self.tournament, tournament_round=3).first()
        self.assertIsNotNone(game_round3)
        self.assertEqual(self.tournament.current_round, 3)

        # final round 종료 (user1 vs user4에서 user1 최종 승리 가정)
        finish_game(game_round3.game_id.id, user1_score=3, user2_score=2)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.round_3_winner, self.user1)
        self.assertEqual(self.tournament.status, 'finished')
