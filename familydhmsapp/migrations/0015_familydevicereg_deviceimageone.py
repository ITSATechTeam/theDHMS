# Generated by Django 4.1.7 on 2023-11-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familydhmsapp', '0014_remove_familydevicereg_deviceuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='familydevicereg',
            name='deviceImageOne',
            field=models.ImageField(blank=True, null=True, upload_to='productImage/'),
        ),
    ]
