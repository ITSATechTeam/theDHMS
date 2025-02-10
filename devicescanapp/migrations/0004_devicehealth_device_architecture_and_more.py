# Generated by Django 4.2 on 2024-12-17 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devicescanapp', '0003_devicehealth_devicelocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicehealth',
            name='device_architecture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devicehealth',
            name='operating_system_version',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devicehealth',
            name='ram_size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devicelocation',
            name='deviceLocationISP',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
