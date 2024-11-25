from django.test import TestCase
from django.utils import timezone
from users.models import User
from ..models import PingPongHistory
from ..utils import end_game  # 경로에 따라 조정


class EndGameFunctionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

    def test_end_game_winner_user1(self):
        started_at = timezone.now()
        ended_at = timezone.now()
        game_record = end_game(
            user1=self.user1,
            user2=self.user2,
            user1_score=21,
            user2_score=19,
            gamemode='normal',
            started_at=started_at,
            ended_at=ended_at
        )
        self.assertEqual(game_record.winner, self.user1)
        self.assertEqual(game_record.user1_score, 21)
        self.assertEqual(game_record.user2_score, 19)

    def test_end_game_draw(self):
        started_at = timezone.now()
        ended_at = timezone.now()
        game_record = end_game(
            user1=self.user1,
            user2=self.user2,
            user1_score=20,
            user2_score=20,
            gamemode='normal',
            started_at=started_at,
            ended_at=ended_at
        )
        self.assertIsNone(game_record.winner)
        self.assertEqual(game_record.user1_score, 20)
        self.assertEqual(game_record.user2_score, 20)

    def test_end_game_invalid_scores(self):
        started_at = timezone.now()
        ended_at = timezone.now()
        with self.assertRaises(ValueError):
            end_game(
                user1=self.user1,
                user2=self.user2,
                user1_score=-1,  # 유효하지 않은 점수
                user2_score=20,
                gamemode='normal',
                started_at=started_at,
                ended_at=ended_at
            )
