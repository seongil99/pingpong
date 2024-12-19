from rest_framework import serializers

from backend.json_mixin import CamelCaseSerializerMixin


class Vec3Serializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()


class BallSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    id = serializers.IntegerField()
    position = serializers.DictField()
    velocity = Vec3Serializer()
    summon_direction = serializers.BooleanField()
    power_counter = serializers.IntegerField()
    radius = serializers.FloatField()


class gameStateSerializer(CamelCaseSerializerMixin, serializers.Serializer):
    oneName = serializers.CharField()
    twoName = serializers.CharField()
    playerOne = Vec3Serializer()
    playerTwo = Vec3Serializer()
    balls = BallSerializer(many=True)
    score = serializers.DictField()


class InMemoryGameStateSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    game_state = gameStateSerializer()
    is_single_player = serializers.BooleanField()
    ai_KeyState = serializers.DictField()
    gameStart = serializers.BooleanField()
    clients = serializers.DictField()
