from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.friends.models import Friend
from users.friends.serializers import (
    FriendRequestWithOtherUserSerializer,
    UserRelationSerializer,
    FriendSerializer,
)
from .serializers import UserSearchSerializer
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer


@extend_schema(tags=["users"])
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserProfileSerializer,
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses=UserProfileSerializer,
    )
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

User = get_user_model()


@extend_schema(
    summary="Search Users",
    description="Search for users by email or username. 유저 검색",
    tags=["users"],
)
class UserSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to search
    serializer_class = UserSearchSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]  # Use the search filter backend
    search_fields = ["email", "username"]  # Fields to search in


@extend_schema(
    summary="Search Users who are friendable",
    description="Search for users by email or username who are not already friends with the current user. Excludes blocked users.",
    tags=["users"],
)
class SearchFriendableView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "username"]

    def get_queryset(self):
        # Get all friends for the current user (both as user1 and user2)
        friends_users = Friend.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        ).values_list(
            "user1", "user2"
        )  # Get both user1 and user2

        # Flatten the result to a single list and exclude the current user's ID
        friend_ids = [
            user for pair in friends_users for user in pair
        ]  # Flattening pairs into a list

        # Exclude users that are already in the friends list
        queryset = User.objects.exclude(id__in=friend_ids).exclude(
            id=self.request.user.id
        )
        return queryset
