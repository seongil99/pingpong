from django.urls import path, include
from accounts.views import (
    HelloView,
)
from .views import CustomTokenVerifyView
# from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    # path('', include(tf_urls)),
    path('mfa/', include("accounts.two_factor_auth.urls")),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('token/custom_verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    path('oauth2/', include('accounts.oauth2.urls')),
]
