# Generated by Django 4.2 on 2023-05-27 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0028_rename_maintaindeviceuser_maintenancerequest_maintaindeviceuserfirstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='currentMonth',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]