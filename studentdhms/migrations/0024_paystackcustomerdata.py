# Generated by Django 5.1 on 2024-09-01 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentdhms', '0023_alter_studentdhmssignup_student_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayStackCustomerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integration', models.CharField(max_length=200)),
                ('customer_code', models.CharField(max_length=200)),
                ('student_email_address', models.EmailField(max_length=200)),
                ('paystack_id', models.CharField(max_length=200)),
                ('paystack_identified', models.CharField(max_length=200)),
                ('paystack_identifications', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-edited_at', '-created_at'],
            },
        ),
    ]
