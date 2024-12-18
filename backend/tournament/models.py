from django.db import models
from django.contrib.auth import get_user_model

from pingpong_history.models import PingPongHistory

User = get_user_model()


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'pending'),
            ('ongoing', 'ongoing'),
            ('finished', 'finished')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    current_round = models.IntegerField(
        default=0,
        choices=[
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
        ]
    )  # 0: pending, 1: 1st round, 2: 2nd round, 3: 3rd round
    round_1_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="round_1_winner", null=True)
    round_2_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="round_2_winner", null=True)
    round_3_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="round_3_winner", null=True)


class TournamentMatchParticipants(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_participant_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_participant_user2")
    user3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_participant_user3")
    user4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_participant_user4")

    class Meta:
        unique_together = ['tournament', 'user1', 'user2', 'user3', 'user4']


class TournamentParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    is_ready = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'tournament']


class TournamentGame(models.Model):
    game_id = models.OneToOneField(PingPongHistory, on_delete=models.CASCADE)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    tournament_round = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)])
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_game_player_one")
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_game_player_two")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'pending'),
            ('ongoing', 'ongoing'),
            ('finished', 'finished'),
        ]
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user_1} is playing against {self.user_2} in a tournament game at {self.created_at}"


class TournamentQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ['user']
