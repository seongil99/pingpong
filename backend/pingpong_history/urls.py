from django.urls import path
from .views import (
    PingPongHistoryAllView,
    PingPongHistoryViewByHistoryId,
    PingPongHistoryAllViewByUserId,
)

urlpatterns = [
    path("", PingPongHistoryAllView.as_view(), name="pingpong-history-all"),
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
]
