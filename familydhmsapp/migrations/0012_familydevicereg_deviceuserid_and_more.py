# Generated by Django 4.1.7 on 2023-11-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familydhmsapp', '0011_faultydevicestrend'),
    ]

    operations = [
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
