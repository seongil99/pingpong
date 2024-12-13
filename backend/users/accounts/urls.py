from django.urls import path, include
from .views import IsLoginView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("verify/", IsLoginView.as_view(), name="is_login"),
    path("oauth2/", include("users.accounts.oauth2.urls")),
    path("mfa/", include("users.accounts.two_factor_auth.urls")),
]
