from django.urls import path

from .views import (
    TournamentAllView,
    TournamentViewByTournamentId,
    TournamentViewByUserId,
)

urlpatterns = [
    path("", TournamentAllView.as_view(), name="tournament-all"),
    path(
        "<int:tournament_id>/",
        TournamentViewByTournamentId.as_view(),
        name="tournament-by-id",
    ),
    path(
        "user/<int:user_id>/",
        TournamentViewByUserId.as_view(),
        name="tournament-by-user",
    ),
]