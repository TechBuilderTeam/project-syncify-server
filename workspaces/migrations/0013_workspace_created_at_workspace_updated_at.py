# Generated by Django 5.0.6 on 2024-05-24 20:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0012_timeline_remaining_time_alter_task_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workspace',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
