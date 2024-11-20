from django.urls import path, include
from friends.views import (
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
    path("friends/", friend_list, name="friend-list"),
    path("friends/<int:pk>/", friend_detail, name="friend-detail"),
    path(
        "friend-requests/<int:id>/",
        FriendRequestActionView.as_view(),
        name="friend-request-action",
    ),
    path("friend-requests", FriendRequestView.as_view(), name="friend-request"),
]
