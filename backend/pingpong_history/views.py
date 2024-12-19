from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if data.get("gamemode") == GameMode.PVE.value:
            data["user1"] = request.user.id  # Assign the user's ID, not the instance

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Call the regular create method for other gamemodes
        return super().create(request, *args, **kwargs)


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
