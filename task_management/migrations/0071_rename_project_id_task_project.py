# Generated by Django 4.2.1 on 2023-10-21 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0070_project_priority'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='project_id',
            new_name='project',
        ),
    ]