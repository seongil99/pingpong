from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.users.manages import UserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_totp_device(sender, instance, created, **kwargs):
#     if created:
#         TOTPDevice.objects.create(user=instance, name="default device")


admin.site.register(User)