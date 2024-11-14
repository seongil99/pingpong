from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

@method_decorator(login_required, name='dispatch')
class friends(APIView):
	def get(self, request) -> JsonResponse:
		user = request.user
		friends = user.friends.all()
		return JsonResponse({'friends': [friend for friend in friends]})

	def put(self, request) -> JsonResponse:
		user = request.user
		friend_id = request.data['friend_id']
		friend = User.objects.get(id=friend_id)
		user.friends.add(friend)
		return JsonResponse({'message': f'{friend} added to friends list'})