# Generated by Django 4.2.7 on 2024-08-03 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_orcamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='entrada',
        ),
    ]
