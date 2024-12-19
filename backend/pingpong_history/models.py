from django.core.validators import MinValueValidator
from django.db import models
from users.models import User
from ingame.enums import GameMode


class PingPongHistory(models.Model):
    """
    탁구 게임 기록 모델
    """
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pingpong_games_as_user1",
        null=True,
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pingpong_games_as_user2",
        null=True,
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pingpong_games_won",
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField(auto_now_add=True, null=False)
    ended_at = models.DateTimeField(null=True)
    user1_score = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    user2_score = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    gamemode = models.CharField(max_length=255)
    longest_rally = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    average_rally = models.FloatField(null=True, validators=[MinValueValidator(0)])
    tournament_id = models.ForeignKey(
        "tournament.Tournament",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    option_selector = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    multi_ball = models.BooleanField(default=None, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user1", "user2", "started_at"], name="unique_game_per_time"
            ),
            models.CheckConstraint(
                check=~models.Q(user1=models.F("user2")), name="prevent_self_play"
            ),
        ]
        ordering = ["-started_at"]

    def save(self, *args, **kwargs):
        if self.gamemode == GameMode.PVE.value:
            self.user2 = None
        elif self.user1.id > self.user2.id:
            # 사용자 순서 교환
            self.user1, self.user2 = self.user2, self.user1
            # 점수도 교환 (필요한 경우)
            self.user1_score, self.user2_score = self.user2_score, self.user1_score
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1} vs {self.user2} - {self.winner} won"


class PingPongRound(models.Model):
    match = models.ForeignKey(PingPongHistory, on_delete=models.CASCADE, related_name='rounds')
    user1_score = models.IntegerField(default=0)
    user2_score = models.IntegerField(default=0)
    rally = models.IntegerField(default=0)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ["start"]
