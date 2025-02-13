# Generated by Django 5.1.2 on 2024-12-17 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pingpong_history', '0005_remove_pingponghistory_user1_powerball_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PingPongRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1_score', models.IntegerField(default=0)),
                ('user2_score', models.IntegerField(default=0)),
                ('rally', models.IntegerField(default=0)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='pingpong_history.pingponghistory')),
            ],
            options={
                'ordering': ['start'],
            },
        ),
    ]
