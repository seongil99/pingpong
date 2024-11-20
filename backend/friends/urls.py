from django.urls import path, include
from friends.views import (
    FriendRequestActionView,
    FriendRequestView,
    FriendsView,
)

urlpatterns = [
    path("friends/", FriendsView.as_view(), name="friends-list"),
    path(
        "friend-requests/<int:id>/",
        FriendRequestActionView.as_view(),
        name="friend-request-action",
    ),
    path("friend-requests", FriendRequestView.as_view(), name="friend-request"),
]
