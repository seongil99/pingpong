from rest_framework import serializers
from pingpong_history.models import PingPongHistory


class PingPongHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PingPongHistory
        fields = "__all__"
        read_only_fields = [
            "id",
            # "user1",
            "user2",
            "winner",
            "started_at",
            "ended_at",
            "user1_score",
            "user2_score",
            "longest_rally",
            "average_rally",
            # "gamemode",
        ]
        extra_kwargs = {"user1": {"required": False}}  # Makes the field optional


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


class PingPongEventSerializer:
    """
    별도의 Serializer class가 아니라 헬퍼 형태로 PingPongHistory queryset을 기반으로
    EventSerializer용 데이터를 만드는 헬퍼.
    """

    @staticmethod
    def build_event_from_histories(histories):
        # histories: PingPongHistory의 queryset 또는 list
        # eventType 결정
        if not histories:
            raise ValueError("No histories provided")

        first = histories[0]
        if first.tournament_id:
            eventType = "tournament"
            eventId = first.tournament_id_id
        else:
            eventType = "match"
            eventId = first.id

        # startDate, endDate 계산
        startDate = min(h.started_at for h in histories)
        endDates = [h.ended_at for h in histories if h.ended_at is not None]
        endDate = max(endDates) if endDates else startDate

        matches_data = []
        for h in histories:
            # round명: "user1 vs user2"
            user1 = h.user1
            user2 = h.user2
            round_name = f"{user1.username if user1 else 'Unknown'} vs {user2.username if user2 else 'Unknown'}"

            # players 정보
            user1_status = None
            user2_status = None
            if h.user1_score is not None and h.user2_score is not None:
                if h.user1_score == h.user2_score:
                    user1_status = "draw"
                    user2_status = "draw"
                else:
                    if h.winner == user1:
                        user1_status = "winner"
                        user2_status = "loser"
                    elif h.winner == user2:
                        user1_status = "loser"
                        user2_status = "winner"

            players = []
            if user1:
                players.append({
                    "playerId": user1.id,
                    "name": user1.username,
                    "score": h.user1_score if h.user1_score is not None else 0,
                    "status": user1_status
                })
            if user2:
                players.append({
                    "playerId": user2.id,
                    "name": user2.username,
                    "score": h.user2_score if h.user2_score is not None else 0,
                    "status": user2_status
                })

            matches_data.append({
                "matchId": h.id,
                "round": round_name,
                "startTime": h.started_at,
                "endTime": h.ended_at,
                "players": players
            })

        event_data = {
            "eventId": eventId,
            "eventType": eventType,
            "startDate": startDate,
            "endDate": endDate,
            "matches": matches_data
        }

        return event_data
