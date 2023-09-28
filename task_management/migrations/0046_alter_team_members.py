# Generated by Django 4.2.1 on 2023-09-28 17:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task_management', '0045_remove_team_team_members_team_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='team_member', through='task_management.TeamMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
