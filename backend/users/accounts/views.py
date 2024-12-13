from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from drf_spectacular.utils import extend_schema

import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class IsLoginView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {"message": "user is logged in"}
        return Response(content, status=200)
