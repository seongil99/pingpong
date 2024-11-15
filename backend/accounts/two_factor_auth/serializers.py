from rest_framework import serializers

class MFAStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['enabled', 'disabled'])