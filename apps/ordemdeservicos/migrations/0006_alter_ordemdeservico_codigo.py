# Generated by Django 4.2.7 on 2024-06-04 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordemdeservicos', '0005_alter_ordemdeservico_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemdeservico',
            name='codigo',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True, verbose_name='Código'),
        ),
    ]