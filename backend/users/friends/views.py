from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Friend
from .serializers import (
    FriendSerializer,
    AddFriendSerializer,
)

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
    create=extend_schema(
        tags=["Friends"], summary="Update Friend", description="Update a friend."
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

    def get_serializer_class(self):
        # This allows you to return different serializers for different actions
        if self.action == "create":
            return AddFriendSerializer  # For POST requests (creating a friend request)
        return FriendSerializer  # For GET or other actions (responding with friendship data)

    def get_queryset(self):
        # Filter queryset to include only the friends of the currently logged-in user
        return Friend.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Custom create logic (if needed)
        user = request.user
        friend = User.objects.get(id=request.data["friend"])
        Friend.objects.create(user=user, friend=friend)
        return super().create(request, *args, **kwargs)
