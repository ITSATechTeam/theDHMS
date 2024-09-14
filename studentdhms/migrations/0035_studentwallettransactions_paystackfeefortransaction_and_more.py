# Generated by Django 5.1 on 2024-09-10 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0034_studentwallettransactions_partneraccountbank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwallettransactions',
            name='paystackFeeForTransaction',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionAuthCode',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionCardType',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionDateFromPaystack',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionNarration',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='transactionPOSData',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
