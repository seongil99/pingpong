from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MatchRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_requests_user")
    gamemode = models.CharField(max_length=255)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} requested a 1vs1 match in {self.gamemode} mode at {self.requested_at}"
