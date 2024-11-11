from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import HttpResponse
from django.template.loader import render_to_string
from accounts.oauth2.adapter import FortyTwoAdapter

oauth2_login = OAuth2LoginView.adapter_view(FortyTwoAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoAdapter)

class FortyTwoLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = FortyTwoAdapter
    callback_url = "https://localhost/oauth2/redirect"
    client_class = OAuth2Client
