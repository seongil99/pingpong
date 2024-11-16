from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Friend


class FriendRequestSerializer(serializers.Serializer):
    target_user = serializers.IntegerField(
        help_text="The ID of the target user to send a friend request to.",
        required=True,
        validators=[MinValueValidator(0)],
    )

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'user1', 'user2', 'requester', 'status', 'created_at']
