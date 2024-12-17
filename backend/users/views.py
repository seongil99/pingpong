from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import filters, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from users.friends.models import Friend
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import UserSearchSerializer
from .serializers import UserProfileSerializer

import logging

logger = logging.getLogger("django")


@extend_schema(tags=["users"])
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        responses=UserProfileSerializer,
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})  # context 추가
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses=UserProfileSerializer,
    )
    def patch(self, request):
        user = request.user
        data = request.data.copy()

        import os

        if "avatar" in data:
            extension = os.path.splitext(data["avatar"].name)[1]  # 파일의 확장자 추출
            data["avatar"].name = f"{user.username}_profile{extension}"

        serializer = UserProfileSerializer(data=data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

User = get_user_model()


@extend_schema(
    tags=["users"],
)
class UserSearchView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to search
    serializer_class = UserProfileSerializer
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
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "username"]

    def get_queryset(self):
        # Get all friends for the current user (both as user1 and user2)
        friends_users = Friend.objects.filter(Q(user=self.request.user)).values_list(
            "friend_user"
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
