from django.urls import path, include
from .views import get_csrf_token

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
]