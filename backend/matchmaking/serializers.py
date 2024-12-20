from rest_framework import serializers


class PVEMatchRequestSerializer(serializers.Serializer):
    multi_ball = serializers.BooleanField(
        required=True,
    )
