from rest_framework import serializers
import logging

from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger("django")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "is_verified",
            "is_online",
            "last_seen",
            "wins",
            "loses",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_online",
            "last_seen",
            "wins",
            "loses",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "avatar": {"required": False},
            "is_verified": {"required": False},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.is_verified = validated_data.get("is_verified", instance.is_verified)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_account_active"]
        read_only_fields = ["id", "username"]


class CurrentGameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField(allow_null=True)
    status = serializers.ChoiceField(choices=["pending", "ongoing", "finished"], allow_null=True)
    round = serializers.IntegerField(allow_null=True)
