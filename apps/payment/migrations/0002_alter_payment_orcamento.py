# Generated by Django 4.2.7 on 2024-08-03 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orcamentos', '0006_alter_orcamento_validade'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='orcamento',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='orcamentos.orcamento'),
        ),
    ]
