# Generated by Django 4.2 on 2024-06-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0005_remove_studentdhmssignup_student_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdhmssignup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentdhmssignup',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
