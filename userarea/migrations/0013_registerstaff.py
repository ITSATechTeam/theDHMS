# Generated by Django 4.2 on 2023-04-23 14:33

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userarea', '0012_maintenancerequest_maintaindevicelocation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceuser', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceuserphonenumber', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceuseremail', models.CharField(blank=True, max_length=200, null=True)),
                ('countries', django_countries.fields.CountryField(max_length=746, multiple=True)),
            ],
        ),
    ]
