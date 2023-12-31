# Generated by Django 4.2 on 2023-06-05 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0020_alter_devicecountperpage_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenancerequest',
            old_name='MaintainDeviceUser',
            new_name='MaintainDeviceType',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='devicelocation',
            new_name='StaffID',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='deviceuseremail',
            new_name='staff_email',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='deviceuserfirstname',
            new_name='staff_firstname',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='deviceuserlastname',
            new_name='staff_lastname',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='deviceuserphonenumber',
            new_name='staff_location',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='staffDevice',
            new_name='staff_phonenumber',
        ),
        migrations.RenameField(
            model_name='staffdataset',
            old_name='staffDeviceName',
            new_name='staff_role',
        ),
        migrations.RemoveField(
            model_name='staffdataset',
            name='staffDeviceStatus',
        ),
        migrations.RemoveField(
            model_name='staffdataset',
            name='staffrole',
        ),
        migrations.AddField(
            model_name='addedmaintenancecomments',
            name='commenterEmailAddress',
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='deviceregisterupload',
            name='CompanyUniqueCode',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='deviceregisterupload',
            name='staffUserID',
            field=models.CharField(default='None', max_length=1500),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='CompanyUniqueCode',
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainDeviceUserDepartment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainDeviceUserFirstname',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainDeviceUserLastname',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainRequesterEmailAddress',
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='maintenancerequest',
            name='currentMonth',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='staffdataset',
            name='CompanyUniqueCode',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='devicecountperpage',
            name='count',
            field=models.CharField(default='10', max_length=10),
        ),
    ]
