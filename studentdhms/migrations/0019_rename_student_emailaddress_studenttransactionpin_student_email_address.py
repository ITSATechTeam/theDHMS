# Generated by Django 5.1 on 2024-08-31 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0018_studenttransactionpin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studenttransactionpin',
            old_name='student_emailAddress',
            new_name='student_email_address',
        ),
    ]
