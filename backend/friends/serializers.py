from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Friend

User = get_user_model()

class FriendRequestSerializer(serializers.Serializer):
    target_user = serializers.IntegerField(
        help_text="The ID of the target user to send a friend request to.",
        required=True,
        validators=[MinValueValidator(0)],
    )

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["id", "user1", "user2", "requester", "status", "created_at"]


from drf_spectacular.utils import extend_schema_field
from accounts.users.serializers import UserSerializer
from .models import Friend


class FriendRequestWithOtherUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the friend request list that includes the 'other_user' annotation.
    """

    other_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Friend  # Replace with your actual FriendRequest model
        fields = ("id", "requester", "status", "created_at", 'other_user')
        read_only_fields = (
            "id",
            "requester",
            "status",
            "created_at",
            "other_user",
        )

    @extend_schema_field(UserSerializer)
    def get_other_user(self, obj):
        """
        This method returns the User instance for the other_user.
        """
        
        if obj.user1 == self.context["request"].user:
            return UserSerializer(obj.user2).data
        return UserSerializer(obj.user1).data

