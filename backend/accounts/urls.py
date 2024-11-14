from django.urls import path, include
from accounts.views import (
    HelloView,
    CustomLoginView,
)
from .two_factor_auth.views import get_user_otp_qrcode, mfaStatus, verifyMFAview
from .views import CustomTokenVerifyView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('two-factor-auth/qrcode/', get_user_otp_qrcode.as_view(), name='2fa_qr'),
    path('token/custom_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    path('two-factor-auth/', mfaStatus.as_view(), name='2fa_enable'),
    path('two-factor-auth/verifications/', verifyMFAview, name='2fa_verify'),
    path('custom_login/', CustomLoginView.as_view(), name='login'),
    path('oauth2/', include('accounts.oauth2.urls')),
]
