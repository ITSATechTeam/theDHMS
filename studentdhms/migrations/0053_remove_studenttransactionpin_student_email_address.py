# Generated by Django 5.1 on 2024-09-19 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0052_remove_studentwallettransactions_studentid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studenttransactionpin',
            name='student_email_address',
        ),
    ]
