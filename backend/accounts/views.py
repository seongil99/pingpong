from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
    )
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from .adapter import FortyTwoAdapter
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.error import Error
from accounts.detail import Detail
from datetime import timedelta
from .models import User

import pyotp
import qrcode
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=['accounts'])
class HelloView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


@extend_schema(tags=['2FA'])
class get_user_otp_qrcode(LoginRequiredMixin, APIView):
    def get(self, request):
        user = request.user
        if not user.mfa_secret:
            return Response({'error': Error.MFA_NOT_ENABLED.value }, status=status.HTTP_400_BAD_REQUEST)
        
        userDB = User.objects.get(email=user.email)
        otp_uri = pyotp.totp.TOTP(userDB.mfa_secret).provisioning_uri(
            name=userDB.email,
            issuer_name="Django",
        )
        
        qr = qrcode.make(otp_uri)
        
        response = HttpResponse(content_type='image/png')
        qr.save(response, format='PNG')
        
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response

@extend_schema(tags=['accounts'])
class CustomTokenVerifyView(APIView):
    
    def post(self, request, *args, **kwargs):
        # Get the token from cookies
        token = request.COOKIES.get('ft_transcendence-app-auth')

        if not token:
            return Response({"detail": Error.NO_TOKEN_IN_COOKIE.value }, status=status.HTTP_401_UNAUTHORIZED)

        # Use JWTAuthentication to verify the token
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": Detail.TOKEN_IS_VALID.value}, status=status.HTTP_200_OK)
    
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
            return JsonResponse({"success": False, "message": Error.USER_NOT_FOUND.value }, status=status.HTTP_400_BAD_REQUEST)
        if verify_2fa_otp(request.user, otp):
            return JsonResponse({"success": True, "message": Detail.MFA_ENABLED.value }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success": False, "message": Error.INVALID_OTP.value }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        """
            Disable 2FA for the user
        """
        user = request.user
        user.mfa_enabled = False
        user.save()
        return JsonResponse({"success": True, "message": Detail.MFA_DISABLED.value }, status=status.HTTP_200_OK)    

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
        user = User.objects.get(id = user_id)
        otp = request.data.get('otp')
        if verify_2fa_otp(user, otp):
            return setTokenCookie2fa(user)
        else:
            return JsonResponse({"success": False, "message": Error.INVALID_OTP.value }, status=status.HTTP_400_BAD_REQUEST)

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

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user = self.get_user_from_serializer(request.data)
        
        if not user:
            return self.get_response()
        
        if user.mfa_enabled:
            two_factor_token = TwoFactorToken.for_user(user)
            response = JsonResponse({
                'message': 'Password verified. Proceed with 2FA.',
                'mfa_enabled': user.mfa_enabled,
            })
            response.set_cookie(
                '2fa_token', 
                str(two_factor_token), 
                max_age=300,  # 5 minutes
                httponly=True, 
                secure=True
            )
            return response
        else:
            return super().get_response()
            
    def get_user_from_serializer(self, data):
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            return serializer.validated_data['user']
        return None

import requests
import urllib
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class Test(SocialLoginView):
    adapter_class = FortyTwoAdapter
    client_class = OAuth2Client
    callback_url = 'http://localhost/api/v1/accounts/callback/'
    

oauth2_login = OAuth2LoginView.adapter_view(FortyTwoAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoAdapter)
