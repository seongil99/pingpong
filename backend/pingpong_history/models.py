from django.db import models
from accounts.users.models import User


class PingPongHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)
    user1_score = models.IntegerField()
    user2_score = models.IntegerField()
    gamemode = models.CharField(max_length=255)

    class Meta:
        constraints = [
            # Enforce uniqueness and ordering (user1 < user2) for a unique game
            models.CheckConstraint(
                check=models.Q(user1__lt=models.F('user2')),
                name='user1_lt_user2'
            )
        ]

    def __str__(self):
        return f"{self.user1} vs {self.user2} - {self.winner} won"
