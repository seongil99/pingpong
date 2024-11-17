from django.urls import path, include
from rest_framework.routers import DefaultRouter
from friends.views import (
    SendFriendRequestView,
    FriendRequestActionView,
    FriendsViewSet,
    UserSearchView,
)

router = DefaultRouter()
router.register(r"users/friends", FriendsViewSet, basename="friends")

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("users/friends/requests", SendFriendRequestView.as_view(), name="friend-request"),
    path("users/friends/requests/<int:id>/", FriendRequestActionView.as_view(), name="friend-request-action"),
    # path("users/search/", )
]

urlpatterns += router.urls