# Generated by Django 4.2 on 2023-05-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0026_alter_deviceregisterupload_deviceworkingcondition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceregisterupload',
            name='deviceworkingcondition',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Bad', 'Bad')], default='Good', max_length=300, null=True),
        ),
    ]