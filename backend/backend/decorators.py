# my_app/decorators.py
from django.http import JsonResponse

def spa_login_required(view_func):
    """
    Custom decorator to check if the user is authenticated for SPA.
    Returns a JSON response with error code 401 if the user is not logged in.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
