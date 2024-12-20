from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models, transaction
from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from pingpong_history.models import PingPongHistory
from tournament.models import TournamentGame, Tournament, TournamentMatchParticipants
from users.friends.models import Friend
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import UserSearchSerializer, CurrentGameSerializer
from .serializers import UserProfileSerializer

import logging

logger = logging.getLogger("django")


@extend_schema(tags=["users"])
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        responses=UserProfileSerializer,
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(
            user, context={"request": request}
        )  # context 추가
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses=UserProfileSerializer,
    )
    def patch(self, request):
        user = request.user
        data = request.data.copy()

        import os

        if "avatar" in data:
            extension = os.path.splitext(data["avatar"].name)[1]  # 파일의 확장자 추출
            data["avatar"].name = f"{user.username}_profile{extension}"

        serializer = UserProfileSerializer(
            user, data=data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

User = get_user_model()


@extend_schema(
    tags=["users"],
)
class UserSearchView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to search
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]  # Use the search filter backend
    search_fields = ["email", "username"]  # Fields to search in


@extend_schema(
    summary="Search Users who are friendable",
    description="Search for users by email or username who are not already friends with the current user. Excludes blocked users.",
    tags=["users"],
)
class SearchFriendableView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "username"]

    def get_queryset(self):
        # Get all friends for the current user (both as user1 and user2)
        friends_users = Friend.objects.filter(Q(user=self.request.user)).values_list(
            "friend_user"
        )  # Get both user1 and user2

        # Flatten the result to a single list and exclude the current user's ID
        friend_ids = [
            user for pair in friends_users for user in pair
        ]  # Flattening pairs into a list

        # Exclude users that are already in the friends list
        queryset = User.objects.exclude(id__in=friend_ids).exclude(
            id=self.request.user.id
        )
        return queryset


@extend_schema(tags=["users"])
class MyCurrentGameView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=CurrentGameSerializer,
    )
    @transaction.atomic
    def get(self, request):
        user = request.user

        # 1. Tournament에서 pending 혹은 ongoing 상태의 사용자 게임 조회
        tournament_ids = TournamentMatchParticipants.objects.filter(
            Q(user1=user) | Q(user2=user) | Q(user3=user) | Q(user4=user)
        ).values_list("tournament_id", flat=True)

        # 진행 중인 가장 최근 토너먼트 가져오기
        tournament = (
            Tournament.objects.filter(
                tournament_id__in=tournament_ids, status__in=["pending", "ongoing"]
            )
            .order_by("-created_at")
            .first()
        )

        if tournament:
            # 해당 토너먼트의 가장 최근 TournamentGame
            tournament_game = (
                TournamentGame.objects.filter(tournament_id=tournament)
                .order_by("-created_at")
                .first()
            )

            # Tournament는 있지만 TournamentGame이 없으면 204 반환
            if tournament_game is None:
                return Response(status=204)

            data = {
                "game_id": tournament_game.game_id_id,  # PK 정수 값
                "tournament_id": tournament_game.tournament_id_id,  # PK 정수 값
                "status": tournament_game.status,
                "round": (
                    tournament_game.tournament_round
                    if tournament_game.tournament_round is not None
                    else None
                ),
            }
            serializer = CurrentGameSerializer(data)
            return Response(serializer.data)

        # 2. TournamentGame이 없으면 PingPongHistory에서 대기중(pending) 혹은 진행중(ongoing)인 게임 조회
        normal_game = (
            PingPongHistory.objects.filter(
                (Q(user1=user) | Q(user2=user)),
                winner__isnull=True,
                ended_at__isnull=True,
            )
            .order_by("-started_at")
            .first()
        )

        if normal_game and normal_game.ended_at is not None:
            status = "ongoing"
            data = {
                "game_id": normal_game.id,
                "tournament_id": None,
                "status": status,
                "round": None,
            }
            serializer = CurrentGameSerializer(data)
            return Response(serializer.data)

        # 어떤 게임도 없는 경우 No Content 반환
        return Response(status=204)
