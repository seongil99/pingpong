from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class OTPTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the OTP token from cookies
        token = request.COOKIES.get('otp_token')
        if not token:
            raise AuthenticationFailed('No OTP token provided.')

        # Validate the token and get the user
        try:
            # Use the get_user method from JWTAuthentication to validate the token
            user = self.get_user(validated_token=token)
        except Exception:
            raise AuthenticationFailed('Invalid OTP token.')

        # Return the user and the token
        return user, token