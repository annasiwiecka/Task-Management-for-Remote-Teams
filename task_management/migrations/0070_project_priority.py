# Generated by Django 4.2.1 on 2023-10-19 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0069_team_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_management.priority'),
        ),
    ]