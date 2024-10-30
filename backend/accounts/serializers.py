from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
import pyotp
from .models import User

class CustomUserDetailsSerializer(UserDetailsSerializer):
    # Add custom fields
    # profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    # bio = serializers.CharField(source='profile.bio', read_only=True)
    # Add any additional fields you want here

    mfa_enabled = serializers.SerializerMethodField()
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_verified',
            'otp_required',
            'mfa_enabled',
        ]  # Include new fields
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_mfa_enabled(self, obj):
        return bool(obj.mfa_secret)
    
class CustomRegisterSerializer(RegisterSerializer):
    # Add custom fields
    # profile_picture = serializers.ImageField(write_only=True)
    # bio = serializers.CharField(write_only=True)
    # Add any additional fields you want here

    def custom_signup(self, request, user):
        # user.profile.profile_picture = self.validated_data.get('profile_picture')
        # user.profile.bio = self.validated_data.get('bio')
        # user.profile.save()
        # Add any additional fields you want here
        user.mfa_secret = pyotp.random_base32()
        user.save()
