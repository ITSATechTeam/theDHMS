# Generated by Django 4.2 on 2024-06-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0007_studentdhmssignup_student_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdhmssignup',
            name='student_phone',
        ),
        migrations.AddField(
            model_name='studentdhmssignup',
            name='student_school',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
