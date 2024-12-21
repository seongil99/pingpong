import logging

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.auth import get_user_model
from django.db import transaction

from users.serializers import UserStatusSerializer
from users.accounts.utils import setAccessToken

User = get_user_model()


logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class VerifyView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {"message": "user is logged in"}
        return Response(content, status=200)


@extend_schema(
    tags=["accounts"],
)
class AccountActiveView(GenericAPIView):
    """
    유저 계정 활성화 상태를 변경합니다.
    """

    queryset = User.objects.all()
    serializer_class = UserStatusSerializer

    @extend_schema(
        summary="Update the status of the logged in user.",
        description="only takes True as is_active value.",
        request=UserStatusSerializer,
        responses={200: UserStatusSerializer},
    )
    def patch(self, request, *args, **kwargs):
        userId = request.session.get("userId")
        user = request.user

        with transaction.atomic():
            user.refresh_from_db()
            is_account_active = request.data.get(
                "is_account_active", user.is_account_active
            )
            if is_account_active is not True:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid value for is_account_active.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_account_active = is_account_active
            user.save()
        response = Response(self.get_serializer(user).data)
        logger.info(f"response: {request.session['access']}")
        logger.info(f"response: {request.session['refresh']}")
        setAccessToken(
            request, response, request.session["access"], request.session["refresh"]
        )

        return response

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.is_account_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                "message": "user is not logged in",
            }
            return Response(content, status=200)
        content = {
            "is_logged_in": True,
            "status": "logged in",
            "message": "user is logged in",
        }
        return Response(content, status=200)
