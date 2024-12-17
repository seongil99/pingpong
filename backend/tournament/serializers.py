from rest_framework import serializers
from tournament.models import (
    Tournament,
    TournamentGame,
    TournamentMatchParticipants,
    TournamentParticipant,
)


class PlayerSerializer(serializers.Serializer):
    playerId = serializers.IntegerField()
    name = serializers.CharField()
    score = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False, allow_null=True)


class MatchSerializer(serializers.Serializer):
    matchId = serializers.IntegerField()
    round = serializers.CharField()
    startTime = serializers.DateTimeField()
    endTime = serializers.DateTimeField(allow_null=True)
    players = PlayerSerializer(many=True)


class EventSerializer(serializers.Serializer):
    eventId = serializers.IntegerField()
    eventType = serializers.CharField()
    startDate = serializers.DateTimeField()
    endDate = serializers.DateTimeField()
    matches = MatchSerializer(many=True)


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
