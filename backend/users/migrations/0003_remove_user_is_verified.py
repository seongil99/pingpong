# Generated by Django 5.1.2 on 2024-11-16 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_is_2fa_verified_remove_user_mfa_enabled_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
