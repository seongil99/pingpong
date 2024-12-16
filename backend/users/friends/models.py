from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q, UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
    )
    friend_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend_user",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "friend_user"], name="unique_friendship"),
        ]
