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
    path("users/", include("friends.urls")),
    path("users/", include("users.urls")),
]

# urlpatterns += router.urls
