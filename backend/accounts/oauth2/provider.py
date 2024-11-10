from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
# from .adapter import FortyTwoAdapter
import logging

logger = logging.getLogger(__name__)


class FortyTwoProvider(OAuth2Provider):
    id = "fortytwo"
    name = "42 OAuth"
    # oauth2_adapter_class = FortyTwoAdapter

    package = 'allauth.socialaccount.providers.oauth2'

    @classmethod
    def get_package(cls):
        return 'accounts'

    def extract_uid(self, data):
        # 유저 고유 ID를 추출하는 방식
        logger.info(f"Data: {data}")
        return str(data["id"])

    def extract_common_fields(self, data):
        # 유저 정보 중 공통 필드 추출
        logger.info(f"Data: {data}")
        return dict(
            username=data.get("login"),
            email=data.get("email"),
            name=data.get("login"),
        )


provider_classes = [FortyTwoProvider]
