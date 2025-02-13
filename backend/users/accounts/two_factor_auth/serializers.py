from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_otp.plugins.otp_totp.models import TOTPDevice

from .error import Errors

import logging
logger = logging.getLogger('django')

class MFAStatusSerializer(serializers.Serializer):
    """
    MFA 상태 GET serializer
    """

    status = serializers.ChoiceField(choices=["enabled", "disabled"])


class OTPVerificationSerializer(serializers.Serializer):
    """
    OTP 인증 request serializer
    """

    otp = serializers.CharField(
        max_length=6,  # Maximum length of the OTP code
        min_length=6,  # Minimum length of the OTP code
        required=True,  # Ensure this field is mandatory
        error_messages={
            "min_length": "The OTP code must be 6 characters long.",
            "max_length": "The OTP code must be 6 characters long.",
            "blank": "The OTP code cannot be empty.",
        },
    )

    def validate_otp_code(self, value):
        # Get the user from the request (or pass it manually)
        user = self.context.get("user")

        # Find the device linked to the user
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if not device:
            logger.info('no device')
            raise ValidationError(Errors.NO_DEVICE.value)

        # Verify OTP code
        if not device.verify_token(value):
            logger.info('invalid otp')
            raise ValidationError(Errors.INVALID_OTP.value)

        return value
