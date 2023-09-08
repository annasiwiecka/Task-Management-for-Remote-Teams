# Generated by Django 4.2.1 on 2023-09-08 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2400)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=30)),
                ('profile_picture', models.CharField(max_length=200, null=True)),
                ('role', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(verbose_name=2400)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team_member', to='task_management.user')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_created', to='task_management.user')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2400)),
                ('deadline', models.DateTimeField()),
                ('priority', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=15)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.user')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.team'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
                ('is_read', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='task_management.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.user')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=40)),
                ('file', models.CharField(max_length=200)),
                ('upload', models.DateTimeField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.task')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_management.user')),
            ],
        ),
    ]
