# my_app/decorators.py
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse, extend_schema
from .error import Error
from .serializers import SimpleResponseSerializer

@extend_schema(
    description="Decorator to check if the user is authenticated for SPA",
    responses={
        401: OpenApiResponse(
            description="Authentication required",
            response=SimpleResponseSerializer,
        ),
    }
    )
def spa_login_required(view_func):
    """
    Custom decorator to check if the user is authenticated for SPA.
    Returns a JSON response with error code 401 if the user is not logged in.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": Error.AUTHENTICATION_REQUIRED.value}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
