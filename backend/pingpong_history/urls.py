from django.urls import path
from .views import (
    PingPongHistoryAllView,
    PingPongHistoryViewByHistoryId,
    PingPongHistoryAllViewByUserId,
    EventView,
)

pingpong_history_list = PingPongHistoryAllView.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

urlpatterns = [
    path("", pingpong_history_list, name="pingpong-history-all"),
    path(
        "user/<int:user_id>/",
        PingPongHistoryAllViewByUserId.as_view(),
        name="pingpong-history-by-user",
    ),
    path(
        "<int:history_id>/",
        PingPongHistoryViewByHistoryId.as_view(),
        name="pingpong-history-by-id",
    ),
    path("event/<str:event_type>/<int:id_value>/", EventView.as_view(), name="event-detail"),
]
