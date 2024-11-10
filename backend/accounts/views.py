from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from accounts.error import Error
from accounts.detail import Detail

import logging

from accounts.two_factor_auth.views import TwoFactorToken

logger = logging.getLogger(__name__)


@extend_schema(tags=['accounts'])
class HelloView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


@extend_schema(tags=['accounts'])
class CustomTokenVerifyView(APIView):

    def post(self, request, *args, **kwargs):
        # Get the token from cookies
        token = request.COOKIES.get('ft_transcendence-app-auth')

        if not token:
            return Response({"detail": Error.NO_TOKEN_IN_COOKIE.value}, status=status.HTTP_401_UNAUTHORIZED)

        # Use JWTAuthentication to verify the token
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": Detail.TOKEN_IS_VALID.value}, status=status.HTTP_200_OK)


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
