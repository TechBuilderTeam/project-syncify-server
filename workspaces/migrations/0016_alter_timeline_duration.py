# Generated by Django 5.0.6 on 2024-05-26 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0015_merge_20240525_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='duration',
            field=models.CharField(blank=True, null=True),
        ),
    ]