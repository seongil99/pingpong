from django.urls import path, include
from friends.views import (
    SendFriendRequestView,
    FriendRequestActionView,
    FriendsView
)

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/friends/", FriendsView.as_view(), name="friends"),
    path("users/friends/requests", SendFriendRequestView.as_view(), name="friend-request"),
    path("users/friends/requests/<int:id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
]
