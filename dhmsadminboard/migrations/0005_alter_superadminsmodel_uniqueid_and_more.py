# Generated by Django 4.2 on 2024-04-12 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhmsadminboard', '0004_alter_superadminsmodel_uniqueid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superadminsmodel',
            name='UniqueID',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='superadminsmodel',
            name='email',
            field=models.EmailField(max_length=300),
        ),
        migrations.AlterField(
            model_name='superadminsmodel',
            name='firstname',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='superadminsmodel',
            name='lastname',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='superadminsmodel',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]
