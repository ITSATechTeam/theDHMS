# Generated by Django 4.1.7 on 2023-11-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familydhmsapp', '0013_remove_familydevicereg_deviceuserid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familydevicereg',
            name='deviceUser',
        ),
        migrations.AddField(
            model_name='familydevicereg',
            name='deviceUserID',
            field=models.CharField(blank=True, default='None', max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='familydevicereg',
            name='deviceuseremail',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='familydevicereg',
            name='deviceuserfullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
