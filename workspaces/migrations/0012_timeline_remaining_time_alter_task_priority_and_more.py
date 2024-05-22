# Generated by Django 5.0.6 on 2024-05-22 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0011_merge_0009_alter_member_role_0010_member_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='remaining_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MID', 'Mid'), ('HIGH', 'High')], default='LOW', max_length=100),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.member'),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='end_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='start_Date',
            field=models.DateField(),
        ),
    ]