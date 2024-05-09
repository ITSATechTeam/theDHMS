# Generated by Django 4.2 on 2024-04-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aichat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIResponsePrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=1000)),
                ('chat_id', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-edited_at', '-created_at'],
            },
        ),
    ]
