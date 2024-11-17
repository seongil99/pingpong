from rest_framework import serializers

class SimpleResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    