from rest_framework.decorators import api_view
from pingpong_history.models import PingPongHistory
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def PVEMatchView(request):
    user = request.user
    PingPongHistory.objects.create(user_1=User.objects.get(id=1))
    return Response("Success", status=status.HTTP_201_CREATED)
