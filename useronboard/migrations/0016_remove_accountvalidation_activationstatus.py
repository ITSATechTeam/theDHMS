# Generated by Django 4.2 on 2024-07-16 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useronboard', '0015_remove_accountvalidation_accountvalidationcode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountvalidation',
            name='activationStatus',
        ),
    ]
