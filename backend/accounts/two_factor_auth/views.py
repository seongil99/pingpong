import pyotp
import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from accounts.error import Error
from datetime import timedelta
from django.conf import settings

from accounts.detail import Detail
from accounts.users.models import User


@extend_schema(tags=['2fa'])
class get_user_otp_qrcode(LoginRequiredMixin, APIView):
    def get(self, request):
        user = request.user
        if not user.mfa_secret:
            return Response({'error': Error.MFA_NOT_ENABLED.value}, status=status.HTTP_400_BAD_REQUEST)

        userDB = User.objects.get(email=user.email)
        otp_uri = pyotp.totp.TOTP(userDB.mfa_secret).provisioning_uri(
            name=userDB.email,
            issuer_name="Django",
        )

        qr = qrcode.make(otp_uri)

        from django.http import HttpResponse
        response = HttpResponse(content_type='image/png')
        qr.save(response, format='PNG')

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response


@extend_schema(tags=['2fa'])
@permission_classes([IsAuthenticated])
class mfaStatus(APIView):
    def post(self, request, *args, **kwargs):
        """
            Enable 2FA for the user
        """
        otp = request.data.get('otp')
        user_email = request.user.email
        if not user_email:
            return JsonResponse({"success": False, "message": Error.USER_NOT_FOUND.value},
                                status=status.HTTP_400_BAD_REQUEST)
        if verify_2fa_otp(request.user, otp):
            return JsonResponse({"success": True, "message": Detail.MFA_ENABLED.value}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success": False, "message": Error.INVALID_OTP.value},
                                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
            Disable 2FA for the user
        """
        user = request.user
        user.mfa_enabled = False
        user.save()
        return JsonResponse({"success": True, "message": Detail.MFA_DISABLED.value}, status=status.HTTP_200_OK)


@extend_schema(tags=['2fa'])
@api_view(['POST'])
def verifyMFAview(request):
    """
        Verify 2FA for the user
    """
    if request.method == 'POST':
        token_str = request.COOKIES.get('2fa_token')
        if not token_str:
            return JsonResponse({'error': '2FA token missing or expired'}, status=403)
        two_factor_token = AccessToken(token_str)
        user_id = two_factor_token['user_id']
        user = User.objects.get(id=user_id)
        otp = request.data.get('otp')
        if verify_2fa_otp(user, otp):
            return setTokenCookie2fa(user)
        else:
            return JsonResponse({"success": False, "message": Error.INVALID_OTP.value},
                                status=status.HTTP_400_BAD_REQUEST)


class TwoFactorToken(AccessToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set a custom expiration for 2FA tokens (e.g., 5 minutes)
        self.set_exp(lifetime=timedelta(minutes=5))


def setTokenCookie2fa(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Create response and set tokens as HttpOnly cookies
    response = JsonResponse({'message': '2FA verified successfully!'}, status=status.HTTP_200_OK)
    response.set_cookie(
        key=settings.REST_AUTH['JWT_AUTH_COOKIE'],
        value=access_token,
        httponly=settings.REST_AUTH['JWT_AUTH_HTTPONLY'],
        secure=settings.JWT_AUTH_COOKIE_SECURE,  # Set to True in production
        samesite=settings.JWT_AUTH_COOKIE_SAMESITE
    )
    response.set_cookie(
        key=settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],
        value=str(refresh),
        httponly=settings.REST_AUTH['JWT_AUTH_HTTPONLY'],
        secure=settings.JWT_AUTH_REFRESH_COOKIE_SECURE,
        samesite=settings.JWT_AUTH_REFRESH_COOKIE_SAMESITE
    )

    return response


def verify_2fa_otp(user, otp):
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        if user.mfa_enabled:
            return True
        user.mfa_enabled = True
        user.save()
        return True
    return False
