# Generated by Django 4.2 on 2023-04-28 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0016_delete_registerstaff_delete_signupuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffdataset',
            name='staffDeviceName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='staffdataset',
            name='staffDeviceStatus',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]