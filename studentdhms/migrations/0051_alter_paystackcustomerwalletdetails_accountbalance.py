# Generated by Django 5.1 on 2024-09-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0050_transferrequests_receiveremail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paystackcustomerwalletdetails',
            name='accountBalance',
            field=models.IntegerField(default=0),
        ),
    ]
