from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=['accounts'])
class HelloView(APIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Cookies: {request.COOKIES}")
        content = {'message': 'Hello, World!'}
        return Response(content)
