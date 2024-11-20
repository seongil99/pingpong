from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/", include("friends.urls")),
    path("users/", include("users.urls")),
]
