from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile
import requests
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
        return str(data["id"])

    def extract_common_fields(self, data):
        # 유저 정보 중 공통 필드 추출
        return dict(
            username=data.get("login"),
            email=data.get("email"),
            name=data.get("login"),
        )

    def extract_extra_data(self, data):
        extra_data = super().extract_extra_data(data)
        image_link = data.get('image', {}).get('link')
        logger.info(f"image_link: {image_link}")
        if image_link:
            extra_data['image_link'] = image_link
        return extra_data


provider_classes = [FortyTwoProvider]


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        logger.info(f"sociallogin.account.provider: {sociallogin.account.provider}")
        pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        logger.info(f"sociallogin.account.provider: {sociallogin.account.provider}")

        if sociallogin.account.provider == 'fortytwo':
            extra_data = sociallogin.account.extra_data
            image_link = extra_data.get('image_link')

            if image_link and not user.avatar:
                try:
                    response = requests.get(image_link)
                    response.raise_for_status()
                    file_extension = image_link.split('.')[-1]  # 확장자 추출
                    user.avatar.save(
                        f'{user.username}_profile.{file_extension}',
                        ContentFile(response.content),
                        save=True
                    )
                    logger.info(f"Profile image saved from {image_link}")
                except Exception as e:
                    # 에러 처리
                    logger.error(f"Failed to save profile image from {image_link}: {e}")

        return user
