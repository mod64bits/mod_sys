from django.db import models
from apps.base.models import BaseModel
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.core.calculos import valor_porcentagem
from apps.orcamentos.models import Orcamento


class Payment(BaseModel):
    FORMA_PAGAMENTO_CHOICE = [
        ("AVISTA", "AVISTA"),
        ("CARTAO", "CARTÃO"),
        ("BOLETO", "BOLETO"),
        ("CONVENIO", "CONVENIO"),
    ]
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=15, choices=FORMA_PAGAMENTO_CHOICE)
    acrecimo = models.DecimalField("Acrécimo", decimal_places=2, max_digits=8, null=True, blank=True)
    entrada = models.BooleanField(default=False)
    valor_entrada = models.DecimalField("Entrada", decimal_places=2, max_digits=8, null=True, blank=True)

    valor_bruto = models.DecimalField("Bruto", decimal_places=2, max_digits=8, null=True, blank=True)
    qt_parcelas = models.IntegerField("Quantidade de Parcelas", default=1)
    valor_acrecimo = models.DecimalField("Valor Acrecimo", decimal_places=2, max_digits=8, null=True, blank=True)
    total_acrecimo = models.DecimalField('Total Acrécimo', decimal_places=2, max_digits=8, null=True, blank=True)
    orcamento = models.OneToOneField(Orcamento, on_delete=models.PROTECT, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.entrada:
            self._meta.get_field('valor_entrada').editable = False
        else:
            self._meta.get_field('valor_entrada').editable = True



    def __str__(self):
        return f"{self.forma_pagamento} - {self.orcamento}"



def update_total_payment(sender, instance, signal, *args, **kwargs):
    paynent = instance
    obj = paynent.orcamento

    if paynent.qt_parcelas > 1:
        obj_valores = valor_porcentagem(paynent.acrecimo, obj.total)
        acrecimo = obj_valores[0]
        total_acrecimo = obj_valores[1]
        paynent.total_acrecimo = total_acrecimo
        paynent.valor_acrecimo = acrecimo
        paynent.save()
        return



