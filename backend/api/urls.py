from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("users/", include("users.urls")),
    path("pingpong-history/", include("pingpong_history.urls")),
    path("tournament/", include("tournament.urls")),
] + debug_toolbar_urls()
