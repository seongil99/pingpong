from django.urls import path, include
from .views import (
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
    path("", friend_list, name="friends-list"),
    path("<int:pk>/", friend_detail, name="friends-detail"),
    path("requests", FriendRequestView.as_view(), name="friend-request"),
]
