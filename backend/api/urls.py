from django.urls import path, include
from friends.views import (
    FriendRequestActionView,
    FriendRequestView,
    UserSearchView,
    FriendsViewSet,
    SearchFriendableView,
)
# from rest_framework.routers import DefaultRouter, SimpleRouter

# router = DefaultRouter()

friend_list = FriendsViewSet.as_view(
    {
        "get": "list",
    }
)

friend_detail = FriendsViewSet.as_view(
    {
        'get': 'retrieve',
        "delete": "destroy",
    }
)

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("users/friends/", friend_list, name="friends-list"),
    path("users/friends/<int:pk>/", friend_detail, name="friends-detail"),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("users/friend-requests", FriendRequestView.as_view(), name="friend-request"),
    path(
        "users/friend-requests/<int:id>/",
        FriendRequestActionView.as_view(),
        name="friend-request-action",
    ),
    path(
        "users/search/friendable",
        SearchFriendableView.as_view(),
        name="search-friendable",
    ),
]

# urlpatterns += router.urls
