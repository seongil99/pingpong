from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from users.serializers import UserProfileSerializer
from .models import Friend

User = get_user_model()


class UserRelationSerializer(serializers.Serializer):
    target_user = serializers.IntegerField(
        help_text="The ID of the target user to send a friend request to.",
        required=True,
        validators=[MinValueValidator(0)],
    )

    def validate_target_user(self, value):
        # Check if the target user is the same as the current authenticated user
        user = self.context["request"].user
        if value == user.id:
            raise serializers.ValidationError("Target ID cannot be urself.")
        return value


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["id", "user", "friend", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    
class AddFriendSerializer(serializers.Serializer):
    target_user = serializers.IntegerField(
        help_text="The ID of the target user to send a friend request to.",
        required=True,
        validators=[MinValueValidator(0)],
    )

    def validate_target_user(self, value):
        # Check if the target user is the same as the current authenticated user
        user = self.context["request"].user
        if value == user.id:
            raise serializers.ValidationError("Target ID cannot be urself.")
        return value