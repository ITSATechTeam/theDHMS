# Generated by Django 4.0.5 on 2023-03-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignupUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=1500, null=True)),
                ('lastname', models.CharField(blank=True, max_length=1500, null=True)),
                ('email', models.EmailField(blank=True, max_length=1500, null=True)),
            ],
        ),
    ]
