# Generated by Django 5.1.2 on 2024-10-11 08:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='OauthId',
            fields=[
                ('oauth_id', models.AutoField(primary_key=True, serialize=False)),
                ('provider', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
