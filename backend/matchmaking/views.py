from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pingpong_history.models import PingPongHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class PVEMatchView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user
        try:
            history = PingPongHistory.objects.create(user_1=user, gamemode="PVE")
            history.save()
            history_id = history.id
            data = {
                "status"
                "history_id": history_id,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "error": str(e),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
