from django.urls import path, include

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/", include("friends.urls")),
    path("users/", include("users.urls")),
]

