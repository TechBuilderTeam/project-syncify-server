# Generated by Django 5.0.6 on 2024-05-26 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0016_alter_timeline_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]