# Generated by Django 5.1.2 on 2024-12-09 13:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pingpong_history', '0002_alter_pingponghistory_ended_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='pingponghistory',
            name='user1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pingpong_games_as_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pingponghistory',
            name='user2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pingpong_games_as_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]
