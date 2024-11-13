from django.urls import path, include
# from two_factor.views import SetupView
# from two_factor.urls import urlpatterns as tf_urls
from .views import (
    mfa,
    qrcode_display,
)

urlpatterns = [
    path('', mfa.as_view(), name='mfa'),
    path('qrcode/', qrcode_display, name='qrcode'),
]
