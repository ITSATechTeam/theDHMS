# Generated by Django 5.1 on 2024-09-11 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0037_registerpaystackcustomers_customercode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionCustomerCode',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionCustomerPhone',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionID',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
