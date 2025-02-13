from django.db import models
from django.contrib.auth import get_user_model
from ingame.enums import GameMode

from pingpong_history.models import PingPongHistory

User = get_user_model()


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "pending"),
            ("ongoing", "ongoing"),
            ("finished", "finished"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    current_round = models.IntegerField(
        default=0,
        choices=[
            (0, 0),
            (1, 1),
            (2, 2),
        ],
    )  # 0: pending, 1: 1st round, 2: 2nd round, 3: 3rd round
    current_game = models.IntegerField(default=1)
    round_1_winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="round_1_winner", null=True
    )
    round_2_winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="round_2_winner", null=True
    )
    round_3_winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="round_3_winner", null=True
    )
    multi_ball = models.BooleanField(default=None, null=True, blank=True)
    option_selector = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="option_selector", null=True
    )


class TournamentMatchParticipants(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tournament_participant_user1"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tournament_participant_user2"
    )
    user3 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tournament_participant_user3"
    )
    user4 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tournament_participant_user4"
    )

    class Meta:
        unique_together = ["tournament", "user1", "user2", "user3", "user4"]


class TournamentParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    is_ready = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "tournament"]


class TournamentGame(models.Model):
    game_id = models.OneToOneField(PingPongHistory, on_delete=models.CASCADE)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    tournament_round = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)])
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tournament_game_player_one",
        null=True,
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tournament_game_player_two",
        null=True,
    )
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "pending"),
            ("ongoing", "ongoing"),
            ("finished", "finished"),
        ],
    )

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        # user_2가 None이 아닐 때만 순서 변경 로직 실행
        if self.user_1 is not None and self.user_2 is not None:
            if self.user_1.id > self.user_2.id:
                # 사용자 순서 교환
                self.user_1, self.user_2 = self.user_2, self.user_1
                # 점수도 교환 (필요한 경우)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_1} is playing against {self.user_2} in a tournament game at {self.created_at}"


class TournamentQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["user"]
