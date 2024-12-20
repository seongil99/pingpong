from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pingpong_history.models import PingPongHistory
from django.contrib.auth import get_user_model

from .serializers import PVEMatchRequestSerializer

User = get_user_model()


@extend_schema(tags=["matchmaking"])
class PVEMatchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PVEMatchRequestSerializer,
        responses=
        {
            201: {
                "type": "object",
                "properties": {
                    "game_id": {
                        "type": "integer",
                        "description": "Game ID for the PVE match"
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        }
    )
    @transaction.atomic
    def post(self, request):
        """
        PVE 매치를 생성하는 엔드포인트입니다.
        - `multi_ball`: 멀티볼 옵션을 활성화할지 여부를 지정합니다.
        """
        user = request.user
        serializer = PVEMatchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        multi_ball = serializer.validated_data.get("multi_ball")
        try:
            history = PingPongHistory.objects.create(user1=user, gamemode="PVE", multi_ball=multi_ball)
            history.save()
            history_id = history.id
            data = {
                "game_id": history_id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "error": str(e),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
