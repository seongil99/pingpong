from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import filters
from .serializers import FriendRequestWithOtherUserSerializer
from rest_framework.generics import GenericAPIView

from .models import Friend
from .serializers import (
    FriendSerializer,
    FriendRequestSerializer,
    UserSearchSerializer,
)
from .error import FriendError
from .detail import FriendDetail

from common.error import Error
from common.pagination import StandardLimitOffsetPagination


User = get_user_model()
# Create your views here.


@extend_schema(
    tags=["Friends"],
)
class FriendRequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Accept a Friend Request",
        description="This endpoint allows a user to accept a friend request from another user. "
        "The request must be in 'PENDING' status. If the request does not exist or is already accepted, "
        "an error will be returned.",
        responses={
            200: OpenApiResponse(
                description="Friend request accepted successfully.",
                response=FriendRequestWithOtherUserSerializer,
            ),
            404: OpenApiResponse(
                description="User or friend request not found.", response=str
            ),
            400: OpenApiResponse(
                description="Request is not in 'PENDING' status or already accepted.",
                response=str,
            ),
        },
        request=None,  # No request body; just use the ID in the URL
    )
    def patch(self, request, id):

        try:
            friend_request = Friend.objects.filter(id=id).first()
            if friend_request is None:
                return Response({"error": FriendError.REQ_NOT_EXIST.value}, status=404)
            if friend_request.status != Friend.PENDING:
                return Response(
                    {"error": FriendError.INVALID_REQUEST.value}, status=400
                )
        except Friend.DoesNotExist:
            return Response({"error": FriendError.REQ_NOT_EXIST.value}, status=404)

        friend_request.status = Friend.ACCEPTED
        friend_request.save()
        serializer = FriendRequestWithOtherUserSerializer(
            friend_request, context={"request": request}
        )
        return Response(serializer.data, status=200)

    @extend_schema(
        summary="Reject a friend request",
        description="Reject a friend request",
        responses={
            200: {
                "description": "Friend request rejected successfully.",
                "response": {
                    "application/json": {
                        "example": {"message": FriendDetail.REQUEST_REJECTED.value}
                    }
                },
            },
            404: {
                "description": "Friend request not found or not in the correct state.",
                "response": {
                    "application/json": {
                        "example": {"error": FriendError.REQ_NOT_EXIST.value}
                    }
                },
            },
        },
    )
    def delete(self, request, id):
        user = request.user
        try:
            # Attempt to get the friend request (pending status and requester must match)
            friend_request = Friend.objects.get(id=id)
            if friend_request.user1 != user and friend_request.user2 != user:
                return Response({"error": Error.PERMISSION_DENIED.value}, status=401)

            if friend_request.status != Friend.PENDING:
                return Response(
                    {"error": FriendError.INVALID_REQUEST.value}, status=400
                )
        except Friend.DoesNotExist:
            # Return error if the friend request doesn't exist or doesn't match the criteria
            return Response({"error": FriendError.DOES_NOT_EXIST.value}, status=404)

        # Reject the friend request by deleting the entry from the database
        friend_request.delete()

        # Return a success message
        return Response({"message": FriendDetail.REQUEST_REJECTED.value}, status=200)


from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.generics import RetrieveUpdateDestroyAPIView


@extend_schema_view(
    list=extend_schema(summary="List Friends", description="List friends for the authenticated user."),
    retrieve=extend_schema(summary="Retrieve Friend", description="Retrieve a friend."),
    destroy=extend_schema(summary="Unfriend or Unblock", description="Unfriend a user."),
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
            status=Friend.ACCEPTED,
        )
        return friends
    
    # @extend_schema(
    #     request=None,
    #     responses={200: FriendRequestWithOtherUserSerializer},
    # )
    # def get(self, request):
    #     """
    #     Return the list of friends for the authenticated user.
    #     """
    #     friends = self.get_queryset()
    #     print(friends)
    #     paginator = StandardLimitOffsetPagination()
    #     paginated_friends = paginator.paginate_queryset(friends, request)
    #     serializer = FriendRequestWithOtherUserSerializer(
    #         paginated_friends, many=True, context={"request": request}
    #     )
    #     return paginator.get_paginated_response(serializer.data)


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
        summary="List Friend Requests",
        description="List friend requests for the authenticated user. Type has to be specified to filter the requests.",
        parameters=[
            OpenApiParameter(
                name="type",
                type=str,
                enum=["sent", "received"],
                description="Filter by type of friend request: 'sent' or 'received'.",
                required=False,
            )
        ],
        responses={
            200: FriendRequestWithOtherUserSerializer,
        },
    )
    def get(self, request):
        """
        Return the list of pending friend requests, optionally filtered by 'sent' or 'received' type.
        """
        friends = self.get_queryset()
        # Apply additional filtering based on the 'type' query parameter
        type_filter = self.request.query_params.get("type", None)

        if type_filter == "sent":
            # Filter for sent friend requests (requests where the authenticated user is the sender)
            friends = friends.filter(requester=self.request.user)
        elif type_filter == "received":
            # Filter for received friend requests (requests where the authenticated user is the receiver)
            friends = friends.exclude(requester=self.request.user)

        paginator = StandardLimitOffsetPagination()
        paginated_friends = paginator.paginate_queryset(friends, request)
        serializer = FriendRequestWithOtherUserSerializer(
            paginated_friends, many=True, context={"request": request}
        )
        # Serialize the filtered queryset
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Send a Friend Request",
        request=FriendRequestSerializer,
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

        if not FriendRequestSerializer(data=request.data).is_valid():
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
            if existing_friendship.status == Friend.PENDING:
                return Response(
                    {"error": FriendError.REQUEST_ALREADY_SENT.value}, status=400
                )
            if existing_friendship.status == Friend.ACCEPTED:
                return Response(
                    {"error": FriendError.ALREADY_FRIENDS.value}, status=400
                )
            if existing_friendship.status == Friend.BLOCKED:
                return Response(
                    {"error": FriendError.INVALID_REQUEST.value}, status=400
                )

        # Create a new friend request
        friend = Friend.objects.create(
            user1=user1, user2=user2, requester=request.user, status=Friend.PENDING
        )
        serializer = FriendSerializer(friend)

        return Response(serializer.data, status=201)


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

    # @extend_schema(
    #     summary="Search Users",
    #     description="Search for users by email or username.",
    #     responses={200: UserSearchSerializer},
    # )
    # def get(self, request):
    #     """
    #     Return a list of users that can be sent friend requests.
    #     """
    #     users = self.filter_queryset(self.get_queryset())
    #     serializer = UserSearchSerializer(users, many=True)
    #     return Response(serializer.data)
