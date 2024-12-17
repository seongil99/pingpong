from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from tournament.models import (
    Tournament,
    TournamentMatchParticipants,
)
from tournament.serializers import (
    TournamentSerializer,
    EventSerializer,
    TournamentSessionSerializer,
)

from tournament.utils import build_event_data


@extend_schema(
    responses=TournamentSerializer,
)
class TournamentAllView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


@extend_schema(
    responses=TournamentSerializer,
)
class TournamentViewByTournamentId(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

    def get(self, request, tournament_id):
        # 특정 tournament_id에 해당하는 토너먼트만 필터링
        tournament = Tournament.objects.get(tournament_id=tournament_id)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)

@extend_schema(
    responses=EventSerializer,
)
class TournamentEventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_id):
        # tournament_id 기반으로 이벤트 데이터 구성
        event_data = build_event_data(tournament_id)
        serializer = EventSerializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


@extend_schema(
    responses=TournamentSerializer,
)
class TournamentViewByUserId(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

    def get_queryset(self):
        # 주어진 user_id가 TournamentMatchParticipants 테이블에서
        # user1, user2, user3, user4 중 하나로 포함된 모든 tournament_id를 가져옴
        tournament_ids = TournamentMatchParticipants.objects.filter(
            Q(user1=self.kwargs["user_id"]) |
            Q(user2=self.kwargs["user_id"]) |
            Q(user3=self.kwargs["user_id"]) |
            Q(user4=self.kwargs["user_id"])
        ).values_list('tournament_id', flat=True)
        # 해당 토너먼트들만 필터링하여 반환
        return Tournament.objects.filter(tournament_id__in=tournament_ids)

@extend_schema(
    responses=TournamentSessionSerializer,
)
class TournamentDetailView(APIView):
    def get(self, request, tournament_id):
        # pk를 기반으로 Tournament 객체를 가져옴
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TournamentSessionSerializer(tournament)
        return Response(serializer.data, status=status.HTTP_200_OK)
