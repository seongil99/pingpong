from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from tournament.serializers import PingPongHistorySessionSerializer
from .models import PingPongHistory
from .serializers import PingPongHistorySerializer, PingPongEventSerializer, EventSerializer
from ingame.enums import GameMode


@extend_schema(
    responses=EventSerializer,
    parameters=[
        OpenApiParameter(
            name='event_type',
            description="Event type: 'match' or 'tournament'",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH
        ),
        OpenApiParameter(
            name='id_value',
            description="Match ID or Tournament ID",
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH
        ),
    ]
)
class EventView(APIView):
    """
    특정 match_id 또는 tournament_id를 기반으로 Event 형태의 응답을 반환.
    예:
    - /api/events/match/{match_id}/ -> 해당 PingPongHistory를 단일 match로 반환
    - /api/events/tournament/{tournament_id}/ -> 해당 토너먼트에 속한 모든 PingPongHistory를 tournament로 반환
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_type = self.kwargs.get("event_type")  # "match" 또는 "tournament"
        id_value = self.kwargs.get("id_value")

        if event_type == "match":
            # 단일 match 조회
            try:
                history = PingPongHistory.objects.get(id=id_value)
            except PingPongHistory.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            event_data = PingPongEventSerializer.build_event_from_histories([history])

        elif event_type == "tournament":
            # 해당 tournament_id의 모든 PingPongHistory 조회
            histories = PingPongHistory.objects.filter(tournament_id_id=id_value).order_by("started_at")
            if not histories:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            event_data = PingPongEventSerializer.build_event_from_histories(histories)
        else:
            return Response({"detail": "Invalid event_type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


@extend_schema(
    responses=PingPongHistorySessionSerializer,
)
class PingPongHistoryDetailView(APIView):
    def get(self, request, history_id):
        # pk를 기반으로 Tournament 객체를 가져옴
        try:
            history = PingPongHistory.objects.get(id=history_id)
        except PingPongHistory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PingPongHistorySessionSerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)
