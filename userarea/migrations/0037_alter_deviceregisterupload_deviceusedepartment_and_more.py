# Generated by Django 4.1.7 on 2023-10-25 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0036_delete_loginstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceregisterupload',
            name='deviceusedepartment',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('ICT', 'ICT'), ('HR', 'HR'), ('Administration', 'Administration'), ('Technician', 'Technician'), ('Accounting', 'Accounting'), ('Marketing', 'Marketing'), ('Customer Service', 'Customer Service')], default='None', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='staffdataset',
            name='staff_role',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('ICT', 'ICT'), ('HR', 'HR'), ('Administration', 'Administration'), ('Technician', 'Technician'), ('Accounting', 'Accounting'), ('Marketing', 'Marketing'), ('Customer Service', 'Customer Service')], default='None', max_length=300, null=True),
        ),
    ]
