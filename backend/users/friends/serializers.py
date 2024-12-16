from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Friend
from rest_framework.exceptions import ValidationError
from users.serializers import UserProfileSerializer
from rest_framework.serializers import PrimaryKeyRelatedField, CurrentUserDefault

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
    user = UserProfileSerializer(read_only=True)
    friend_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ["id", "user", "friend_user", "created_at"]
        read_only_fields = ["id", "user", "friend_user", "created_at"]


class AddFriendSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Friend
        fields = ["user", "friend_user"]

    def validate(self, data):
        # Check if the user is trying to add themselves as a friend
        if data["user"] == data["friend_user"]:
            raise serializers.ValidationError("You cannot add yourself as a friend.")
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        friend_user = validated_data["friend_user"]

        # Ensure no duplicate friend request exists
        if Friend.objects.filter(user=user, friend_user=friend_user).exists():
            raise ValidationError("Friendship already exists.")

        return super().create(validated_data)
