# Generated by Django 4.2 on 2023-05-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0023_alter_maintenancerequest_maintainstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceregisterupload',
            name='devicestatus',
            field=models.CharField(blank=True, choices=[('Healthy', 'Healthy'), ('Critical', 'Critical'), ('Faulty', 'Faulty')], default='Healthy', max_length=300, null=True),
        ),
    ]