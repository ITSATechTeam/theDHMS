# Generated by Django 5.1 on 2024-09-30 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0056_studentmaintenancerequest_maintenance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwallettransactions',
            name='StudentID',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
