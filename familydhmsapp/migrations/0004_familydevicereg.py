# Generated by Django 4.1.7 on 2023-11-16 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('familydhmsapp', '0003_familyregister_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDeviceReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devicekind', models.CharField(default='None', max_length=1500)),
                ('devicebrand', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceOS', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceyearofpurchase', models.CharField(blank=True, max_length=200, null=True)),
                ('devicename', models.CharField(blank=True, max_length=200, null=True)),
                ('devicemacaddress', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceipaddress', models.CharField(blank=True, max_length=1500, null=True)),
                ('devicedepreciationrate', models.CharField(blank=True, max_length=1500, null=True)),
                ('deviceid', models.CharField(blank=True, max_length=1500, null=True)),
                ('savetimedata', models.CharField(blank=True, max_length=1500, null=True)),
                ('registeredMonth', models.CharField(blank=True, max_length=1500, null=True)),
                ('weekNumberSaved', models.CharField(blank=True, max_length=1500, null=True)),
                ('FamilyUniqueCode', models.CharField(blank=True, max_length=130, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-edited_at', '-created_at'],
            },
        ),
    ]
