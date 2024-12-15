from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .serializers import FriendRequestWithOtherUserSerializer
from rest_framework.generics import GenericAPIView

from .models import Friend
from .serializers import (
    FriendSerializer,
    UserRelationSerializer,
)
from .error import FriendError
from .detail import FriendDetail

from common.error import Error
from common.pagination import StandardLimitOffsetPagination


User = get_user_model()
# Create your views here.

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view


@extend_schema_view(
    list=extend_schema(
        tags=["Friends"],
        summary="List Friends",
        description="List friends for the authenticated user.",
    ),
    retrieve=extend_schema(
        tags=["Friends"], summary="Retrieve Friend", description="Retrieve a friend."
    ),
    destroy=extend_schema(
        tags=["Friends"], summary="Unfriend a friend", description="Unfriend a user."
    ),
)
class FriendsViewSet(viewsets.ModelViewSet):
    """
    A viewset to list friends for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestWithOtherUserSerializer

    def get_queryset(self):
        """
        Return a list of friends for the authenticated user.
        """
        friends = Friend.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user),
        )
        return friends


@extend_schema(
    tags=["Friends"],
)
class FriendRequestView(GenericAPIView):
    """
    A viewset to list friend requests for the authenticated user.
    """

    queryset = Friend.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return a list of friends for the authenticated user.
        """
        friends = Friend.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user),
            status=Friend.PENDING,
        )
        return friends

    @extend_schema(
        summary="Send a Friend Request",
        request=UserRelationSerializer,
        responses={
            201: OpenApiResponse(
                description="Friend request successfully sent.",
                response=FriendSerializer,
            ),
            400: OpenApiResponse(
                description="Bad request - Invalid data or friend request already sent.",
                response={
                    "application/json": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}},
                    }
                },
            ),
            404: OpenApiResponse(
                description="User not found.",
                response={
                    "application/json": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}},
                    }
                },
            ),
        },
    )
    def post(self, request):
        target_user_id = request.data.get("target_user")

        if not UserRelationSerializer(
            data=request.data, context={"request": request}
        ).is_valid():
            return Response({"error": FriendError.INVALID_REQUEST.value}, status=400)

        if not target_user_id:
            return Response({"error": FriendError.EMPTY_ID.value}, status=400)

        target_user = User.objects.filter(id=target_user_id).first()
        if not target_user:
            return Response({"error": Error.USER_NOT_FOUND.value}, status=404)

        # Ensure no duplicate friend requests
        user1, user2 = sorted([request.user, target_user], key=lambda u: u.id)
        existing_friendship = Friend.objects.filter(user1=user1, user2=user2).first()

        if existing_friendship:
            Response({"error": FriendError.REQUEST_ALREADY_SENT.value}, status=400)

        # Create a new friend request
        friend = Friend.objects.create(user1=user1, user2=user2, requester=request.user)
        serializer = FriendSerializer(friend)

        return Response(serializer.data, status=201)
