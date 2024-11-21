from django.urls import path, include
from .views import (
    FriendRequestActionView,
    FriendRequestView,
    FriendsViewSet,
)

friend_list = FriendsViewSet.as_view(
    {
        "get": "list",
    }
)

friend_detail = FriendsViewSet.as_view(
    {
        "get": "retrieve",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("friends/", friend_list, name="friends-list"),
    path("friends/<int:pk>/", friend_detail, name="friends-detail"),
    path(
        "friend-requests/<int:id>/",
        FriendRequestActionView.as_view(),
        name="friend-request-action",
    ),
    path("friend-requests", FriendRequestView.as_view(), name="friend-request"),
]
