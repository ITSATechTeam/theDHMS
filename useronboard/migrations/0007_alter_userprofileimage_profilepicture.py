# Generated by Django 4.2 on 2023-04-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useronboard', '0006_alter_userprofileimage_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileimage',
            name='profilepicture',
            field=models.ImageField(blank=True, default='profileimages/default.png', null=True, upload_to='profileimages'),
        ),
    ]
