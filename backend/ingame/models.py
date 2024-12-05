from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class OneVersusOneGame(models.Model):
    game_id = models.AutoField(primary_key=True)
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
