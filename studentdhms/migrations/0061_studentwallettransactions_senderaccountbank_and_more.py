# Generated by Django 5.1 on 2024-09-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0060_rename_studentid_studentwallettransactions_senderstudentid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentwallettransactions',
            name='senderAccountBank',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='senderAccountName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='studentwallettransactions',
            name='senderAccountNumber',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
