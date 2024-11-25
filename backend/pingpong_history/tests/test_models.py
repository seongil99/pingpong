from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from pingpong_history.models import PingPongHistory


class PingPongHistoryModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

    def test_create_pingpong_history(self):
        game = PingPongHistory.objects.create(
            user1=self.user1,
            user2=self.user2,
            user1_score=21,
            user2_score=15,
            winner=self.user1,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now()
        )
        self.assertEqual(game.winner, self.user1)
        self.assertEqual(game.user1_score, 21)
        self.assertEqual(game.user2_score, 15)

    def test_winner_can_be_null(self):
        game = PingPongHistory.objects.create(
            user1=self.user1,
            user2=self.user2,
            user1_score=20,
            user2_score=20,
            winner=None,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now()
        )
        self.assertIsNone(game.winner)

    def test_prevent_self_play(self):
        with self.assertRaises(ValidationError):
            game = PingPongHistory(
                user1=self.user1,
                user2=self.user1,
                user1_score=21,
                user2_score=0,
                winner=self.user1,
                gamemode='normal',
                started_at=timezone.now(),
                ended_at=timezone.now()
            )
            game.full_clean()

    def test_user_ordering_in_save(self):
        game = PingPongHistory.objects.create(
            user1=self.user2,  # 의도적으로 순서 반대로 설정
            user2=self.user1,
            user1_score=15,
            user2_score=21,
            winner=self.user1,
            gamemode='normal',
            started_at=timezone.now(),
            ended_at=timezone.now()
        )
        self.assertEqual(game.user1, self.user1)
        self.assertEqual(game.user2, self.user2)
        self.assertEqual(game.user1_score, 21)
        self.assertEqual(game.user2_score, 15)
