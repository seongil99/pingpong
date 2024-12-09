from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class PingPongHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pingpong_games_as_user1",
        null=False,
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pingpong_games_as_user2",
        null=False,
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
        if self.user1.id > self.user2.id:
            # 사용자 순서 교환
            self.user1, self.user2 = self.user2, self.user1
            # 점수도 교환 (필요한 경우)
            self.user1_score, self.user2_score = self.user2_score, self.user1_score
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1} vs {self.user2} - {self.winner} won"
