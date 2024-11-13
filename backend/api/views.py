from django.http import HttpResponse
from django_otp.decorators import otp_required

@otp_required
def test(request):
    return HttpResponse("Hello, world. You're at the polls index.")
