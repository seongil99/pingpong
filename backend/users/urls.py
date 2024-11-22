from django.urls import path, include
from users.views import (
    UserSearchView,
    SearchFriendableView,
)

urlpatterns = [
    path("search/", UserSearchView.as_view(), name="user-search"),
    path(
        "search/friendable/",
        SearchFriendableView.as_view(),
        name="search-friendable",
    ),
]
