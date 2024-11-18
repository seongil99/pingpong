from django.urls import path, include
from rest_framework.routers import DefaultRouter
from friends.views import (
    FriendRequestActionView,
    FriendRequestView,
    UserSearchView,
    FriendsView,
)

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/friends/", FriendsView.as_view(), name="friends-list"),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("users/friend-requests", FriendRequestView.as_view(), name="friend-request"),
    path(
        "users/friend-requests/<int:id>/",
        FriendRequestActionView.as_view(),
        name="friend-request-action",
    ),
    # path("users/search/", )
]
