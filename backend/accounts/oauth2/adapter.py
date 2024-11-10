from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView, OAuth2Adapter
from accounts.oauth2.provider import FortyTwoProvider
import requests
import logging

logger = logging.getLogger(__name__)


class FortyTwoAdapter(OAuth2Adapter):
    provider_id = 'fortytwo'
    authorize_url = "https://api.intra.42.fr/oauth/authorize"
    access_token_url = "https://api.intra.42.fr/oauth/token"
    profile_url = "https://api.intra.42.fr/v2/me"
    provider_class = FortyTwoProvider

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            headers={"Authorization": f"Bearer {token.token}"}
        )
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(FortyTwoAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoAdapter)
