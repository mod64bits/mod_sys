# Generated by Django 4.2.7 on 2024-08-03 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamentos', '0005_alter_orcamento_validade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='validade',
            field=models.DateField(default=datetime.date(2024, 8, 19), verbose_name='Validade'),
        ),
    ]