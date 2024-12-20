from django.urls import path

from .views import PVEMatchView

urlpatterns = [
    path("pve/", PVEMatchView.as_view(), name="pve-match"),
]
