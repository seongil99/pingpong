from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from accounts.users.models import User


class CustomUserDetailsSerializer(UserDetailsSerializer):
    # Add custom fields
    # profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    # bio = serializers.CharField(source='profile.bio', read_only=True)
    # Add any additional fields you want here

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_verified',
        ]  # Include new fields


class CustomRegisterSerializer(RegisterSerializer):
    # Add custom fields
    # profile_picture = serializers.ImageField(write_only=True)
    # bio = serializers.CharField(write_only=True)
    # Add any additional fields you want here

    def custom_signup(self, request, user):
        pass
        # user.profile.profile_picture = self.validated_data.get('profile_picture')
        # user.profile.bio = self.validated_data.get('bio')
        # user.profile.save()
        # Add any additional fields you want here
        # user.mfa_secret = pyotp.random_base32()
        # user.save()


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
