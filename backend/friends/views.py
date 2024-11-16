from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiResponse

from .models import Friend
from .error import FriendError
from .detail import FriendDetail
from common.error import Error


User = get_user_model()
# Create your views here.

class friends(APIView):
    
	authentication_classes = [IsAuthenticated]
    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "target_user": {
                    "type": "integer",
                    "description": "The ID of the target user to send a friend request to."
                }
            },
        },
        responses={
            200: OpenApiResponse(
                description="Friend request successfully sent.",
                content={"application/json": {"type": "object", "properties": {"message": {"type": "string"}}}}
            ),
            400: OpenApiResponse(
                description="Bad request - Invalid data or friend request already sent.",
                content={"application/json": {"type": "object", "properties": {"error": {"type": "string"}}}}
            ),
            404: OpenApiResponse(
                description="User not found.",
                content={"application/json": {"type": "object", "properties": {"error": {"type": "string"}}}}
            ),
        },
        tags=["Friends"],
    )
	def post(self, request):
		target_user_id = request.data.get("target_user")
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
				return Response({"error": FriendError.REQUEST_ALREADY_SENT.value}, status=400)
			if existing_friendship.status == Friend.ACCEPTED:
				return Response({"error": FriendError.ALREADY_FRIENDS.value}, status=400)
			if existing_friendship.status == Friend.BLOCKED:
				return Response({"error": FriendError.INVALID_REQUEST.value}, status=400)
		
		# Create a new friend request
		Friend.objects.create(user1=user1, user2=user2, requester=request.user, status=Friend.PENDING)
		return Response({"message": FriendDetail.REQUEST_SENT.value}, status=201)
    