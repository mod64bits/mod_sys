# Generated by Django 4.2.7 on 2024-08-04 01:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_payment_total_acrecimo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='acrecimo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='Acrécimo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='total_acrecimo',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=16, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Total Acrécimo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='valor_acrecimo',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=16, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Valor Acrecimo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='valor_bruto',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=16, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Bruto'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='valor_entrada',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='Entrada'),
        ),
    ]