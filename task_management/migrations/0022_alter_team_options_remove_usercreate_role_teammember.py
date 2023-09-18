# Generated by Django 4.2.1 on 2023-09-18 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task_management', '0021_team_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'permissions': [('can_manage_team', 'can manage team'), ('can_manage_tasks', 'can manage tasks')]},
        ),
        migrations.RemoveField(
            model_name='usercreate',
            name='role',
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('responsibilities', models.TextField(blank=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
