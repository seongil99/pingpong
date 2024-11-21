from django.urls import path, include
from .views import (
    UserSearchView,
    SearchFriendableView,
    UserBlockedViewset,
    MyProfileView,
)

blocked_user_list = UserBlockedViewset.as_view(
    {
        "get": "list",
        "put": "update",
    }
)

blocked_user_detail = UserBlockedViewset.as_view(
    {
        "get": "retrieve",
        "delete": "destroy",
    }
)


urlpatterns = [
    path("accounts/", include("users.accounts.urls")),
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("", include("users.friends.urls")),
    path("", UserSearchView.as_view(), name="user-search"),
    path(
        "friendable",
        SearchFriendableView.as_view(),
        name="search-friendable",
    ),
    path("blocks/", blocked_user_list, name="blocks-list"),
    path(
        "blocks/<int:pk>/",
        blocked_user_detail,
        name="blocks-detail",
    ),
]
