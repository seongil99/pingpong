from django.urls import path, include
# from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    
    # path('', include(tf_urls)),
]