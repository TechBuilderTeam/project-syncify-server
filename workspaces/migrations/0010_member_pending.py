# Generated by Django 5.0.6 on 2024-05-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0009_alter_member_role_alter_member_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='pending',
            field=models.BooleanField(default=True),
        ),
    ]