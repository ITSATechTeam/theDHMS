# Generated by Django 4.1.7 on 2023-11-02 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0040_staffadlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffadlist',
            old_name='csv_file',
            new_name='staff_csv_file',
        ),
    ]
