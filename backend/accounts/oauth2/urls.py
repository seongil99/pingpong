from django.urls import path

from .views import (
    FortyTwoLogin,
)

urlpatterns = [
    path('fortytwo/login/callback/', FortyTwoLogin.as_view(), name='42-login-callback'),
]
