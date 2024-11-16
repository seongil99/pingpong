from django.urls import path, include
from rest_framework.routers import DefaultRouter
from friends.views import (
    SendFriendRequestView,
    FriendRequestActionView,
    FriendsViewSet
)

router = DefaultRouter()
router.register(r"friends", FriendsViewSet, basename="friends")

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/friends/requests", SendFriendRequestView.as_view(), name="friend-request"),
    path("users/friends/requests/<int:id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
]

urlpatterns += router.urls