from django.urls import path, include
from .views import (
    HelloView,
)

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("hello/", HelloView.as_view(), name="hello"),
    path("oauth2/", include("users.accounts.oauth2.urls")),
    path("mfa/", include("users.accounts.two_factor_auth.urls")),
]
