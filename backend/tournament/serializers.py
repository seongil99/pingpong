from rest_framework import serializers
from tournament.models import (
    Tournament,
    TournamentGame,
    TournamentMatchParticipants,
    TournamentParticipant,
)


class TournamentMatchParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatchParticipants
        fields = [
            "tournament",
            "user1",
            "user2",
            "user3",
            "user4",
        ]
        read_only_fields = [
            "tournament",
            "user1",
            "user2",
            "user3",
            "user4",
        ]


class TournamentSerializer(serializers.ModelSerializer):
    participants = TournamentMatchParticipantsSerializer(many=False, read_only=True)

    class Meta:
        model = Tournament
        fields = [
            "tournament_id",
            "status",
            "created_at",
            "current_round",
            "participants",
        ]
        read_only_fields = [
            "tournament_id",
            "created_at",
            "current_round",
            "status",
        ]


class TournamentGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGame
        fields = "__all__"
        read_only_fields = "__all__"
