from django.urls import path, include
from accounts.views import (
    HelloView,
)

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('mfa/', include("accounts.two_factor_auth.urls")),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('oauth2/', include('accounts.oauth2.urls')),
    path('users/', include('accounts.users.urls')),
]
