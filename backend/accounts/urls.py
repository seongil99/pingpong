from django.urls import path, include
from accounts.views import HelloView
from accounts.provider import FortyTwoProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('oauth2/', include(default_urlpatterns(FortyTwoProvider))),
]