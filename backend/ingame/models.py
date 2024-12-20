from django.db import models
from django.contrib.auth import get_user_model
from pingpong_history.models import PingPongHistory
from ingame.enums import GameMode

User = get_user_model()


# Create your models here.
class OneVersusOneGame(models.Model):
    game_id = models.OneToOneField(
        PingPongHistory,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    user_1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_one"
    )
    user_2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="player_two"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_1} is playing against {self.user_2} in a 1vs1 game at {self.created_at}"

    def save(self, *args, **kwargs):
        # user_2가 None이 아닐 때만 순서 변경 로직 실행
        if self.user_1 is not None and self.user_2 is not None:
            if self.user_1.id > self.user_2.id:
                # 사용자 순서 교환
                self.user_1, self.user_2 = self.user_2, self.user_1
                # 점수도 교환 (필요한 경우)
        super().save(*args, **kwargs)
