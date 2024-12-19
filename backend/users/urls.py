from django.urls import path, include
from .views import (
    UserSearchView,
    SearchFriendableView,
    MyProfileView,
    MyCurrentGameView,
)

user_list = UserSearchView.as_view(
    {
        "get": "list",
    }
)

user_detail = UserSearchView.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = [
    path("", user_list, name="user-search"),
    path("<int:pk>/", user_detail, name="user-detail"),
    path("accounts/", include("users.accounts.urls")),
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("friends/", include("users.friends.urls")),
    path(
        "friendable/",
        SearchFriendableView.as_view(),
        name="search-friendable",
    ),
    path("me/current-game/", MyCurrentGameView.as_view(), name="current-game"),
]
