# Generated by Django 5.1 on 2024-08-30 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0015_rename_student_name_studentmaintenancerequest_device_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentmaintenancerequest',
            old_name='student_id',
            new_name='student_admin_id',
        ),
        migrations.AddField(
            model_name='studentmaintenancerequest',
            name='student_requester_id',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
