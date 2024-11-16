from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from io import BytesIO
from datetime import timedelta
from drf_spectacular.utils import extend_schema

import base64
import pyotp
import qrcode
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@extend_schema(tags=['2fa'])
@method_decorator(login_required, name='dispatch')
class mfa(APIView):
    def get(self, request) -> JsonResponse:
        if self.otp_enabled(request.user):
            return JsonResponse({'status': 'enabled'})
        return JsonResponse({'status': 'disabled'})
        
    def put(self, request) -> JsonResponse:
        user = request.user
        otp_code = request.data.get('otp_code')
        
        logger.info(f'otp_code: {otp_code}')
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if device and device.verify_token(otp_code):
            device.confirmed = True
            device.save()
            return JsonResponse({'status': '2FA enabled successfully'})
        return JsonResponse({'status': 'Invalid OTP code'}, status=400)
    
    def delete(self, request) -> JsonResponse:
        user = request.user
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        
        if device:
            device.delete()
            return JsonResponse({'status': '2FA disabled successfully'})
    
    def post(self, request) -> JsonResponse:
        User = get_user_model()
        userId = request.session.get('userId')
        user = User.objects.get(id=userId)
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        otp_code = request.data.get('otp')
        logger.info(f'otp_code: {otp_code}')
        if device.verify_token(otp_code):
            return self.setJWTToken(request)
        return JsonResponse({'status': 'Invalid OTP code'}, status=400)
        
    
    def otp_enabled(self, user: User) -> bool:
        return user.totpdevice_set.filter(confirmed=True).exists() # confirmed = True means the device is enabled
    
    def setJWTToken(self, request):
        content = {
            'status': 'redirect',
            'url': '/'
        }
        access = request.session.get('access')
        refresh = request.session.get('refresh')
        response = JsonResponse(content, status=200)
        return setAccessToken(request, response, access, refresh)

def setAccessToken(request, response, access: str, refresh: str):
    response.set_cookie(
        settings.REST_AUTH['JWT_AUTH_COOKIE'], 
        access,
        max_age = timedelta(days=1),
        httponly = True    
    )
    response.set_cookie(
        settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],
        refresh,
        max_age = timedelta(days=1),
        httponly = True
    )
    return response

@api_view(['GET'])
@login_required
@extend_schema(tags=['2fa'])
def qrcode_display(request):
    user = request.user
    device = TOTPDevice.objects.filter(user=user).first()
    
    if not device:
        device = TOTPDevice.objects.create(user=user, name='default device', confirmed=False)
    
    base32_key = convert_hex_to_base32(device.key)
    
    totp = pyotp.TOTP(base32_key)
    totp_url = totp.provisioning_uri(user.email, issuer_name='transcendence')
    
    img = qrcode.make(totp_url)
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return JsonResponse({'qrcode': f"data:image/png;base64,{img_base64}"})

def convert_hex_to_base32(hex_key: str) -> str:
    key_bytes = bytes.fromhex(hex_key)
    base32_key = base64.b32encode(key_bytes).decode('utf-8')
    return base32_key
