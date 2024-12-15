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
        fields = ["id", "user1", "user2", "requester", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        """
        Ensure that user1 has the lesser id and user2 has the greater id.
        """
        user1 = data.get("user1")
        user2 = data.get("user2")

        if user1 and user2:
            if user1.id > user2.id:
                # Swap user1 and user2 if necessary
                data["user1"], data["user2"] = user2, user1

        return data


class FriendRequestWithOtherUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the friend request list that includes the 'other_user' annotation.
    """

    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Friend  # Replace with your actual FriendRequest model
        fields = ("id", "requester", "created_at", "other_user")
        read_only_fields = (
            "id",
            "requester",
            "created_at",
            "other_user",
        )

    @extend_schema_field(UserProfileSerializer)
    def get_other_user(self, obj):
        """
        This method returns the User instance for the other_user.
        """

        if obj.user1 == self.context["request"].user:
            return UserProfileSerializer(obj.user2).data
        return UserProfileSerializer(obj.user1).data
