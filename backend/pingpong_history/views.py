from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import PingPongHistory
from .serializers import PingPongHistorySerializer
from ingame.enums import GameMode


@extend_schema(
    responses=PingPongHistorySerializer,
)
class PingPongHistoryAllView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PingPongHistorySerializer
    queryset = PingPongHistory.objects.all()


@extend_schema(
    responses=PingPongHistorySerializer,
)
class PingPongHistoryAllViewByUserId(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PingPongHistorySerializer
    queryset = PingPongHistory.objects.all()

    def get_queryset(self):
        return PingPongHistory.objects.filter(
            user1=self.kwargs["user_id"]
        ) | PingPongHistory.objects.filter(user2=self.kwargs["user_id"])


@extend_schema(
    responses=PingPongHistorySerializer,
)
class PingPongHistoryViewByHistoryId(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PingPongHistorySerializer,
    )
    def get(self, request, history_id):
        history = get_object_or_404(PingPongHistory, id=history_id)
        serializer = PingPongHistorySerializer(history)
        return Response(serializer.data)
