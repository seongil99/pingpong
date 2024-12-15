from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from users.serializers import UserStatusSerializer
from rest_framework import status

from users.accounts.utils import setAccessToken

User = get_user_model()

import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class VerifyView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {"message": "user is logged in"}
        return Response(content, status=200)


@extend_schema(tags=["users"])
class CheckAnonymousView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            content = {
                "is_logged_in": False,
                "status": "anonymous",
                "message": "user is not logged in",
            }
            return Response(content, status=200)
        content = {
            "is_logged_in": True,
            "status": "logged in",
            "message": "user is logged in",
        }
        return Response(content, status=200)
