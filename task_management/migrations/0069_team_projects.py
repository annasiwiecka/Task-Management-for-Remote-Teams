# Generated by Django 4.2.1 on 2023-10-19 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0068_remove_project_team_members_project_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(related_name='teams', to='task_management.project'),
        ),
    ]