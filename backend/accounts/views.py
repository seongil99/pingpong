from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.views import TokenVerifyView
from .models import User

import pyotp
import qrcode
import io
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=['accounts'])
class HelloView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Cookies: {request.COOKIES}")
        content = {'message': 'Hello, World!'}
        return Response(content)

@extend_schema(tags=['2FA'])
class get_user_otp_qrcode(LoginRequiredMixin, APIView):
    def get(self, request):
        user = request.user
        if not user.mfa_secret:
            return Response({'error': '2FA not enabled'}, status=status.HTTP_400_BAD_REQUEST)
        
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
            return Response({"detail": "Token not found in cookies."}, status=status.HTTP_401_UNAUTHORIZED)

        # Use JWTAuthentication to verify the token
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": "Token is valid."})