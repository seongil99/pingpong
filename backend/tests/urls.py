
from django.urls import path, include
from backend.tests import spaLoginRequiredView

urlpatterns = [
    path('login_required/', spaLoginRequiredView, name='login_required'),
]
