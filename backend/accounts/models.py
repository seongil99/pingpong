from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manages import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=255, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    is_2fa_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
admin.site.register(User)

class OauthId(models.Model):
    oauth_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
