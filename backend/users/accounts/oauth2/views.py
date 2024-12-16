from allauth.socialaccount.providers.oauth2.views import (
    OAuth2CallbackView,
    OAuth2LoginView,
)
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .adapter import FortyTwoAdapter
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

import logging

oauth2_login = OAuth2LoginView.adapter_view(FortyTwoAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoAdapter)

logger = logging.getLogger("django")


class OTPTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("otp_token")
        if not token:
            raise AuthenticationFailed("No OTP token provided.")

        # Validate the token
        try:
            user = self.get_user(validated_token=token)
        except Exception:
            raise AuthenticationFailed("Invalid OTP token.")

        return user, token


from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse

# from two_factor_auth.models import PendingToken
from django_otp import user_has_device
from django.conf import settings
from ..two_factor_auth.views import setAccessToken


class FortyTwoLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = FortyTwoAdapter
    callback_url = "https://localhost/oauth2/redirect"
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if request.user.is_authenticated:
            return self.processAuthenticatedUser(request, response)

        # access = response.data["access"]
        # refresh = response.cookies[settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]].value
        # # logger.info(f'here: {refresh}')
        # response.data["refresh"] = ""
        return response

    def processAuthenticatedUser(self, request, response):
        otp_required = user_has_device(request.user)
        logger.info(f"is_active: {request.user.is_account_active}")
        if not otp_required and request.user.is_account_active:
            # OTP 비활성화 = 로그인 성공
            return response
        # OTP 활성화 OTP 인증 필요
        # verified 는 django-otp 가 사용하는 어휘로 otp 인증 여부를 나타낸다
        logger.info(f"response: {response.data}")
        refresh = response.cookies[settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]].value

        request.session["userId"] = request.user.id
        request.session["access"] = response.data["access"]
        request.session["refresh"] = refresh

        if otp_required:
            contents = {"detail": "OTP required", "status": "redirect", "url": "/otp"}
        else:
            contents = {
                "detail": "User is not active",
                "status": "activation_required",  # 요거는 원하는걸로 바꿔줌
            }
        return JsonResponse(contents, status=401)
