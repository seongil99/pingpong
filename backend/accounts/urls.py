from django.urls import path, include
from accounts.views import HelloView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import get_user_otp_qrcode, CustomTokenVerifyView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('2fa_qr/', get_user_otp_qrcode.as_view(), name='2fa_qr'),
    path('token/custom_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
]