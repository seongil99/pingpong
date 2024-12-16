from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError

from .models import Friend
from .serializers import (
    FriendSerializer,
    AddFriendSerializer,
)

from common.error import Error
from common.pagination import StandardLimitOffsetPagination
from rest_framework.response import Response

User = get_user_model()
# Create your views here.

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from .error import FriendError
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter


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
    create=extend_schema(
        tags=["Friends"],
        summary="Add Friend",
        description="Add a friend.",
        request=AddFriendSerializer,
        responses=FriendSerializer,
    ),
)
class FriendsViewSet(viewsets.ModelViewSet):
    """
    A viewset to list friends for the authenticated user.
    """

    queryset = Friend.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer
    pagination_class = StandardLimitOffsetPagination

    def get_queryset(self):
        # Filter queryset to include only the friends of the currently logged-in user
        return Friend.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        friend_user = request.data.get("friend_user")

        # Ensure the user is authenticated
        user = request.user  # The currently authenticated user

        # Prepare data for the serializer
        data = {
            "user": user.id,  # Do not take this from the client, use the authenticated user
            "friend_user": friend_user,
        }

        # Initialize the serializer with the data
        serializer = AddFriendSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            friend = serializer.save()
            response_serializer = FriendSerializer(friend)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
