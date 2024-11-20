from rest_framework import serializers

from accounts.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'avatar',
            'is_verified',
        ]
        read_only_fields = ['id', 'email']
        extra_kwargs = {
            'username': {'required': False},
            'avatar': {'required': False},
            'is_verified': {'required': False},
        }


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
