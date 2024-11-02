from django.urls import path, include
from accounts.provider import FortyTwoProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from accounts.views import (
    HelloView,
    get_user_otp_qrcode,
    CustomTokenVerifyView,
    mfaStatus,
    verifyMFAview,
    CustomLoginView
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import get_user_otp_qrcode, CustomTokenVerifyView, verify_2fa_otp


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('oauth2/', include(default_urlpatterns(FortyTwoProvider))),
    path('two-factor-auth/qrcode/', get_user_otp_qrcode.as_view(), name='2fa_qr'),
    path('token/custom_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    path('two-factor-auth/', mfaStatus.as_view(), name='2fa_enable'),
    path('two-factor-auth/verifications/', verifyMFAview, name='2fa_verify'),
    path('custom_login/', CustomLoginView.as_view(), name='login'),
]