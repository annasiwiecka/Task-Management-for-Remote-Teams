# Generated by Django 4.2.1 on 2023-09-28 18:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task_management', '0057_remove_team_team_members_team_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AddField(
            model_name='team',
            name='team_members',
            field=models.ManyToManyField(blank=True, related_name='teams', through='task_management.TeamMember', to=settings.AUTH_USER_MODEL),
        ),
    ]