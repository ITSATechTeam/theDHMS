# Generated by Django 4.1.7 on 2023-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familydhmsapp', '0008_familymemberreg'),
    ]

    operations = [
        migrations.AddField(
            model_name='familydevicereg',
            name='devicestatus',
            field=models.CharField(blank=True, choices=[('Working', 'Working'), ('Faulty', 'Faulty'), ('Critical', 'Critical')], default='Working', max_length=300, null=True),
        ),
    ]
