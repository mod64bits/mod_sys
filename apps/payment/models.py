from django.db import models
from apps.base.models import BaseModel
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.orcamentos.models import Orcamento

class Payment(BaseModel):
    FORMA_PAGAMENTO_CHOICE = [
        ("AVISTA", "AVISTA"),
        ("CARTAO", "CARTÃO"),
        ("BOLETO", "BOLETO"),
        ("CONVENIO", "CONVENIO"),
    ]
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=15, choices=FORMA_PAGAMENTO_CHOICE)
    acrecimo = models.DecimalField("Acrécimo",  max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    desconto = models.DecimalField("Desconto", max_digits=16, null=True, blank=True, decimal_places=2,
                                   validators=[
                                       MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_desconto = models.DecimalField("Desconto", max_digits=16, null=True, blank=True, decimal_places=2,
                                   validators=[
                                       MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total_desconto = models.DecimalField("Total Desconto", max_digits=16, null=True, blank=True, decimal_places=2,
                                   validators=[
                                       MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    valor_entrada = models.DecimalField("Entrada", max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    valor_bruto = models.DecimalField("Bruto",  max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    qt_parcelas = models.IntegerField("Quantidade de Parcelas", default=1)
    valor_parcelas = models.DecimalField("Valor Parcelas", max_digits=16, null=True, blank=True, decimal_places=2,
                                         validators=[
                                             MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_acrecimo = models.DecimalField("Valor Acrecimo",  max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total = models.DecimalField('Total', decimal_places=2,  max_digits=16, null=True, blank=True, validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    orcamento = models.ForeignKey(
        Orcamento, on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='payment',
        verbose_name="Orcamento"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.forma_pagamento == "AVISTA":
            self._meta.get_field('desconto').hidden  = False
            self._meta.get_field('desconto').hidden  = False

        else:
            self._meta.get_field('desconto').hidden  = True
            self._meta.get_field('desconto').hidden  = True

    def get_absolute_url(self):
        return reverse('orcamentos:orcamento', kwargs={'pk': self.orcamento.id})

    def __str__(self):
        return f"{self.forma_pagamento} - {self.orcamento}"



