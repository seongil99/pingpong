from django.shortcuts import render
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from .serializers import UserSearchSerializer
from friends.models import Friend
from django.db.models import Q

# Create your views here.

User = get_user_model()


@extend_schema(
    summary="Search Users",
    description="Search for users by email or username. 유저 검색",
    tags=["Users"],
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
    tags=["Users"],
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
