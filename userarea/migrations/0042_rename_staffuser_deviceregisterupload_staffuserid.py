# Generated by Django 4.2 on 2023-06-02 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0041_alter_deviceregisterupload_staffuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deviceregisterupload',
            old_name='staffUser',
            new_name='staffUserID',
        ),
    ]
