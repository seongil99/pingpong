from django.urls import path

from .views import (
    TournamentAllView,
    TournamentViewByTournamentId,
    TournamentViewByUserId,
    TournamentEventView,
    TournamentDetailView,
    TestTournamentEventDataCreateView,
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
    path('<int:tournament_id>/event/', TournamentEventView.as_view(), name='tournament-event'),
    path('<int:tournament_id>/detail/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('testcreate/', TestTournamentEventDataCreateView.as_view(), name='testcreate'),
]
