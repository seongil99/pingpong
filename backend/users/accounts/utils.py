from datetime import timedelta
from django.conf import settings


def setAccessToken(request, response, access: str, refresh: str):
    response.set_cookie(
        settings.REST_AUTH["JWT_AUTH_COOKIE"],
        access,
        max_age=timedelta(days=1),
        httponly=True,
    )
    response.set_cookie(
        settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"],
        refresh,
        max_age=timedelta(days=1),
        httponly=True,
    )
    return response
