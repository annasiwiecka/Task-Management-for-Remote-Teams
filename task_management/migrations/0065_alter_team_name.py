# Generated by Django 4.2.1 on 2023-10-11 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0064_auto_20230929_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
