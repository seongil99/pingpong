from rest_framework import serializers
from pingpong_history.models import PingPongHistory


class PingPongHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PingPongHistory
        fields = "__all__"
        # read_only_fields = [
        #     "id",
        #     "user1",
        #     "user2",
        #     "winner",
        #     "started_at",
        #     "ended_at",
        #     "user1_score",
        #     "user2_score",
        #     "longest_rally",
        #     "average_rally",
        #     "gamemode",
        # ]
