from django.urls import path, include
from .views import (
    UserSearchView,
    SearchFriendableView,
    MyProfileView,
)

urlpatterns = [
    path("", UserSearchView.as_view(), name="user-search"),
    path("accounts/", include("users.accounts.urls")),
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("friends/", include("users.friends.urls")),
    path(
        "friendable/",
        SearchFriendableView.as_view(),
        name="search-friendable",
    ),
]
