# Generated by Django 5.0.6 on 2024-05-24 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0013_workspace_created_at_workspace_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
