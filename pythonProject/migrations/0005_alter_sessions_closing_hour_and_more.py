# Generated by Django 5.0.2 on 2024-02-11 15:37

import time
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonProject', '0004_remove_sessions_closing_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='closing_hour',
            field=models.TimeField(default=time.time),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='opening_hour',
            field=models.TimeField(default=time.time),
        ),
    ]
