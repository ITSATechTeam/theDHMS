# Generated by Django 4.2 on 2024-06-09 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0045_alter_devicecountperpage_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='MaintainPriorityStatus',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=300, null=True),
        ),
    ]
