# Generated by Django 4.2 on 2023-05-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0030_maintenancerequest_maintainrequesteremailaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainDeviceType',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainDeviceUserDepartment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='devicecountperpage',
            name='count',
            field=models.CharField(blank=True, default=4, max_length=3, null=True),
        ),
    ]