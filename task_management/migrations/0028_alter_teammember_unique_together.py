# Generated by Django 4.2.1 on 2023-09-28 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0027_alter_team_members_alter_teammember_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set(),
        ),
    ]
