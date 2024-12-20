from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pingpong_history.models import PingPongHistory
from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema(tags=["matchmaking"])
class PVEMatchView(APIView):
    @extend_schema(
        responses={"200": {"history_id": "int"}},
    )
    @transaction.atomic
    def post(self, request):
        user = request.user
        try:
            history = PingPongHistory.objects.create(user_1=user, gamemode="PVE")
            history.save()
            history_id = history.id
            data = {
                "history_id": history_id,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "error": str(e),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
