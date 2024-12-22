from django.urls import path
from .views import (
    PingPongHistoryAllView,
    PingPongHistoryViewByHistoryId,
    PingPongHistoryAllViewByUserId,
    EventView,
    PingPongHistoryDetailView,
    PingPongHistoryIsEndedByGameId,
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
    path("<int:history_id>/detail/", PingPongHistoryDetailView.as_view(), name="pingpong-history-detail"),
    path("<int:game_id>/is-ended/", PingPongHistoryIsEndedByGameId.as_view(), name="pingpong-history-is-ended"),

]
