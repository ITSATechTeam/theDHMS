# Generated by Django 5.0.1 on 2024-02-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhmsadminboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superadminsmodel',
            name='adminaccesslevel',
            field=models.CharField(blank=True, choices=[('ALLAPPS', 'ALLAPPS'), ('ORGDHMS', 'ORGDHMS'), ('FAMILYDHMS', 'FAMILYDHMS')], default='ORGDHMS', max_length=300, null=True),
        ),
    ]
