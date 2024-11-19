from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# Create your models here.
class Friend(models.Model):
    PENDING = 1
    ACCEPTED = 2
    BLOCKED = 3

    FRIEND_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (BLOCKED, "Blocked"),
    ]

    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend1",
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend2",
    )
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="send_request",
    )
    status = models.IntegerField(
        choices=FRIEND_STATUS_CHOICES,
        default=PENDING,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Enforce uniqueness and ordering (user1 < user2) for a unique friendship
            UniqueConstraint(fields=["user1", "user2"], name="unique_friendship"),
            models.CheckConstraint(
                check=Q(user1__lt=models.F("user2")), name="user1_lt_user2"
            ),
        ]

    def __str__(self):
        return (
            f"Friendship between {self.user1} and {self.user2} - Status: {self.status}"
        )
