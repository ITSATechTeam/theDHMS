# Generated by Django 4.2 on 2023-05-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0025_alter_deviceregisterupload_devicestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceregisterupload',
            name='deviceworkingcondition',
            field=models.CharField(blank=True, choices=[('Working', 'Working'), ('Faulty', 'Faulty'), ('Critical', 'Critical')], default='Good', max_length=300, null=True),
        ),
    ]
