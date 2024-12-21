from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from io import BytesIO
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from .detail import Details
from .error import Errors
from django.db import transaction

from common.serializers import SimpleResponseSerializer
from common.error import Error
from .serializers import (
    MFAStatusSerializer,
    OTPVerificationSerializer,
)

from users.accounts.utils import setAccessToken


import base64
import pyotp
import qrcode
import logging

logger = logging.getLogger("django")

User = get_user_model()


@extend_schema(tags=["2fa"])
class mfa(APIView):

    @extend_schema(
        summary="MFA Status",
        description="Get MFA status",
        request=None,
        responses={
            200: OpenApiResponse(
                description="MFA status", response=MFAStatusSerializer
            ),
        },
    )
    def get(self, request) -> JsonResponse:
        if self.otp_enabled(request.user):
            return JsonResponse(
                MFAStatusSerializer({"status": "enabled"}).data, status=200
            )
        return JsonResponse(
            MFAStatusSerializer({"status": "disabled"}).data, status=200
        )

    @extend_schema(
        summary="Enable MFA",
        description="Enable MFA by verifying OTP",
        request=OTPVerificationSerializer,
        responses={
            200: OpenApiResponse(
                description="OTP verified successfully",
                response=SimpleResponseSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid OTP or missing device",
                response=SimpleResponseSerializer,
            ),
        },
    )
    def put(self, request) -> JsonResponse:
        user = request.user
        serializer = OTPVerificationSerializer(
            data=request.data, context={"user": user}
        )

        if serializer.is_valid() == False:
            return JsonResponse(serializer.errors, status=400)

        otp = serializer.validated_data["otp"]
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if device and device.verify_token(otp):
            device.confirmed = True
            device.save()
            return Response(
                {"detail": Details.MFA_ENABLED.value},
                status=status.HTTP_200_OK,
            )

        # If validation fails, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Disable MFA",
        description="Disable MFA after logging in",
        request=None,
        responses={
            200: OpenApiResponse(
                description="MFA disabled successfully",
                response=SimpleResponseSerializer,
            ),
            400: OpenApiResponse(
                description="No device found", response=SimpleResponseSerializer
            ),
        },
    )
    def delete(self, request) -> JsonResponse:
        user = request.user
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

        if device:
            device.delete()
            return JsonResponse(
                SimpleResponseSerializer({"detail": Details.MFA_DISABLED.value}).data,
                status=200,
            )
        return JsonResponse(
            SimpleResponseSerializer({"detail": Errors.NO_DEVICE.value}).data,
            status=400,
        )

    @extend_schema(
        summary="Verify OTP",
        description="Verify OTP code to login using MFA",
        request=OTPVerificationSerializer,
        responses={
            200: OpenApiResponse(
                description="OTP verified successfully",
                response=SimpleResponseSerializer,
            ),
            400: OpenApiResponse(
                description="Invalid OTP or missing device",
                response=SimpleResponseSerializer,
            ),
        },
    )
    def post(self, request) -> JsonResponse:

        serializer = OTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            otp_code = request.data.get("otp")

            userId = request.session.get("userId")
            try:
                user = User.objects.get(id=userId)
            except User.DoesNotExist:
                return JsonResponse({"detail": Error.USER_NOT_FOUND.value}, status=404)

            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
            if not device:
                return JsonResponse({"status": Errors.NO_DEVICE.value}, status=404)

            if device.verify_token(otp_code):
                content = {"status": "redirect", "url": "/"}
                response = Response(content, status=200)
                self.setJWTToken(request, response)
                request.session.clear()
                return response
            return JsonResponse({"status": Errors.INVALID_OTP.value}, status=400)
        return JsonResponse(serializer.errors, status=400)

    def otp_enabled(self, user: User) -> bool:
        return user.totpdevice_set.filter(
            confirmed=True
        ).exists()  # confirmed = True means the device is enabled

    def setJWTToken(self, request, response):
        access = request.session.get("access")
        refresh = request.session.get("refresh")
        setAccessToken(request, response, access, refresh)


@api_view(["GET"])
@extend_schema(
    description="Display QR code for MFA setup",
    tags=["accounts"],
    request=None,
    responses={
        200: OpenApiResponse(
            description="QR code for MFA",
        ),
        401: OpenApiResponse(
            description="User not authenticated",
            response=SimpleResponseSerializer,
        ),
    },
)
@permission_classes([IsAuthenticated])
def qrcode_display(request):
    user = request.user
    with transaction.atomic():
        device = TOTPDevice.objects.filter(user=user).first()

        if not device:
            device = TOTPDevice.objects.create(
                user=user, name="default device", confirmed=False
            )

    base32_key = convert_hex_to_base32(device.key)

    totp = pyotp.TOTP(base32_key)
    totp_url = totp.provisioning_uri(user.email, issuer_name="transcendence")

    img = qrcode.make(totp_url)

    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    return JsonResponse({"qrcode": f"data:image/png;base64,{img_base64}"})


@extend_schema(tags=["2fa"])
class CheckLoginStatusView(APIView):
    def get(self, request):
        if "userId" in request.session:
            return Response({"status": "logged in"}, status=200)
        return Response({"status": "logged out"}, status=401)


def convert_hex_to_base32(hex_key: str) -> str:
    key_bytes = bytes.fromhex(hex_key)
    base32_key = base64.b32encode(key_bytes).decode("utf-8")
    return base32_key
