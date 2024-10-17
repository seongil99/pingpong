from django.urls import path, include
from accounts.views import HelloView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
]