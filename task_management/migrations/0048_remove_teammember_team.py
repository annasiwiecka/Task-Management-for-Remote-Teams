# Generated by Django 4.2.1 on 2023-09-28 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0047_remove_team_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='team',
        ),
    ]