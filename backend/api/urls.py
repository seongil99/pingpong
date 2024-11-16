from django.urls import path, include
from friends.views import (
    SendFriendRequestView,
    FriendRequestActionView
)

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/friends/requests", SendFriendRequestView.as_view(), name="friends"),
    path("users/friends/requests/<int:id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
    # path('', include(tf_urls)),
]
