from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from accounts.users.serializers import UserSerializer

from .models import Friend
from .serializer import (
    FriendSerializer,
    FriendRequestSerializer,
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
class SendFriendRequestView(APIView):

    authentication_classes = [IsAuthenticated]

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
    tags=["Friends"],
)
class FriendRequestActionView(APIView):
    authentication_classes = [IsAuthenticated]

    @extend_schema(
        summary="Accept a Friend Request",
        description="This endpoint allows a user to accept a friend request from another user. "
        "The request must be in 'PENDING' status. If the request does not exist or is already accepted, "
        "an error will be returned.",
        responses={
            200: OpenApiResponse(
                description="Friend request accepted successfully.",
                response=FriendSerializer,
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
        serializer = FriendSerializer(friend_request)
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
                return Response(
                    {"error": Error.PERMISSION_DENIED.value}, status=401
                )
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


@extend_schema(
    tags=["Friends"],
)
class FriendsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset to list friends for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return a list of friends for the authenticated user.
        Friends are determined by the Friend model where the status is 'ACCEPTED'.
        """
        friends = Friend.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user),
            status=Friend.ACCEPTED,
        )
        return friends

    @extend_schema(
        summary="Retrieve Friend List",
        description="Get a list of friends for the authenticated user. "
        "Friends are determined by the Friend model where the status is 'ACCEPTED'.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer(many=True),
                description="List of friends successfully retrieved.",
            ),
            401: OpenApiResponse(
                description="Unauthorized. The user must be authenticated to access this endpoint."
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        # Get the list of friends based on the queryset
        queryset = self.get_queryset()

        # Paginate the results
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(UserSerializer(page, many=True).data)

        # If no pagination applied (e.g., no query parameters), return all results
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
