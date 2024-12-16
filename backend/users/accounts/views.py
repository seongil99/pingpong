from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample

import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class VerifyView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {"message": "user is logged in"}
        return Response(content, status=200)


@extend_schema(
    tags=["users"],
    examples=[
        OpenApiExample(
            "Anonymous User Response",
            value={
                "is_logged_in": False,
                "status": "anonymous",
                "message": "user is not logged in",
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Authenticated User Response",
            value={
                "is_logged_in": True,
                "status": "logged in",
                "message": "user is logged in",
            },
            response_only=True,
            status_codes=["200"],
        ),
    ],
)
class CheckAnonymousView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={"200": {"description": "로그인 상태 확인"}},
    )
    def get(self, request):
        if not request.user.is_authenticated:
            content = {
                "is_logged_in": False,
                "status": "anonymous",
                "message": "user is not logged in"
            }
            return Response(content, status=200)
        content = {
            "is_logged_in": True,
            "status": "logged in",
            "message": "user is logged in"
        }
        return Response(content, status=200)
