from django.urls import path, include

# from two_factor.views import SetupView
# from two_factor.urls import urlpatterns as tf_urls
from .views import (
    mfa,
    qrcode_display,
    CheckLoginStatusView,
)

urlpatterns = [
    path("", mfa.as_view(), name="mfa"),
    path("qrcode/", qrcode_display, name="qrcode"),
    path(
        "check-login-status", CheckLoginStatusView.as_view(), name="check-login-status"
    ),
]
