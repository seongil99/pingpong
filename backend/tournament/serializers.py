from rest_framework import serializers
from tournament.models import (
    Tournament,
    TournamentGame,
    TournamentMatchParticipants,
    TournamentParticipant,
)
from pingpong_history.models import PingPongHistory, PingPongRound
from drf_spectacular.utils import extend_schema_field


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


class PingPongRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingPongRound
        fields = ['user1_score', 'user2_score', 'rally', 'start', 'end']


class PingPongHistorySessionSerializer(serializers.ModelSerializer):
    rounds = PingPongRoundSerializer(many=True, read_only=True)

    class Meta:
        model = PingPongHistory
        fields = [
            'id', 'started_at', 'ended_at', 'user1_score', 'user2_score',
            'gamemode', 'longest_rally', 'average_rally', 'user1', 'user2', 'winner', 'rounds', 'tournament_id'
        ]


class TournamentMatchParticipantsSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatchParticipants
        fields = ['tournament', 'user1', 'user2', 'user3', 'user4']


class TournamentGameSessionSerializer(serializers.ModelSerializer):
    # TournamentGame는 PingPongHistory를 game_id로 갖고 있으므로, 이를 통해 session 정보를 가져올 수 있다.
    session = PingPongHistorySessionSerializer(source='game_id', read_only=True)

    class Meta:
        model = TournamentGame
        fields = [
            'session'
        ]


class TournamentSessionSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    sessions = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = [
            'tournament_id', 'status', 'created_at', 'current_round',
            'participants', 'sessions'
        ]
    @extend_schema_field(TournamentMatchParticipantsSessionSerializer)
    def get_participants(self, obj):
        # TournamentMatchParticipants 테이블에서 해당 Tournament에 해당하는 row를 가져옴
        try:
            participants_obj = TournamentMatchParticipants.objects.get(tournament=obj)
            return {
                "tournament": participants_obj.tournament.tournament_id,
                "user1": participants_obj.user1.id,
                "user2": participants_obj.user2.id,
                "user3": participants_obj.user3.id,
                "user4": participants_obj.user4.id,
            }
        except TournamentMatchParticipants.DoesNotExist:
            return None

    @extend_schema_field(TournamentGameSessionSerializer(many=True))
    def get_sessions(self, obj):
        # TournamentGame에서 해당 토너먼트에 해당하는 게임들(세션들)을 불러옴
        # 각 session은 PingPongHistorySerializer를 통해 직렬화
        games = TournamentGame.objects.filter(tournament_id=obj)
        # games를 통해 PingPongHistorySerializer를 이용한 데이터를 반환
        # TournamentGameSerializer로 한번 감싼 후 session 필드만 빼와도 된다.
        # 여기서는 한번에 session 리스트를 구성
        return [PingPongHistorySessionSerializer(game.game_id).data for game in games]
