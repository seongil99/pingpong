from django.urls import path, include

urlpatterns = [
    path("users/", include("users.urls")),
    path("pingpong-history/", include("pingpong_history.urls")),
    path("tournament/", include("tournament.urls")),
    path("matchmaking/", include("matchmaking.urls")),
]
