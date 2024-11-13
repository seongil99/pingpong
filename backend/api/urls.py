from django.urls import path, include
# from two_factor.urls import urlpatterns as tf_urls
from .views import test

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('test/', test),
    # path('', include(tf_urls)),
]