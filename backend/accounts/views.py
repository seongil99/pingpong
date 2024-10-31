from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

# Create your views here.
class HelloView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
