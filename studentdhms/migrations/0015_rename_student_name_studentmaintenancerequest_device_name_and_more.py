# Generated by Django 5.1 on 2024-08-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0014_studentmaintenancerequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentmaintenancerequest',
            old_name='student_name',
            new_name='device_name',
        ),
        migrations.RenameField(
            model_name='studentmaintenancerequest',
            old_name='student_password',
            new_name='maintenance_description',
        ),
        migrations.RenameField(
            model_name='studentmaintenancerequest',
            old_name='student_school',
            new_name='maintenance_issue',
        ),
        migrations.RemoveField(
            model_name='studentmaintenancerequest',
            name='student_email',
        ),
        migrations.RemoveField(
            model_name='studentmaintenancerequest',
            name='student_phone',
        ),
        migrations.RemoveField(
            model_name='studentmaintenancerequest',
            name='user',
        ),
        migrations.AddField(
            model_name='studentmaintenancerequest',
            name='maintenance_priority_level',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentmaintenancerequest',
            name='student_id',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
