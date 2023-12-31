# Generated by Django 4.2 on 2023-04-22 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userarea', '0008_deleteddevices_delete_registerstaff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceregisterupload',
            name='staffUser',
        ),
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaintainDeviceName', models.CharField(blank=True, max_length=3, null=True)),
                ('MaintainDeviceMAC_ID', models.CharField(blank=True, max_length=3, null=True)),
                ('MaintainDeviceID', models.CharField(blank=True, max_length=3, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-edited_at', '-created_at'],
            },
        ),
    ]
