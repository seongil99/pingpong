from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

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
        read_only_fields = ["id", "email"]
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
