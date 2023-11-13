from django.db import models

from apps.base.models import BaseModel


class Cliente(BaseModel):
    TIPO_CLIENTE_CHOICE = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    ]

    tipo = models.CharField('Tipo', max_length=4, choices=TIPO_CLIENTE_CHOICE, default="CPF")
    nome = models.CharField('Nome', max_length=100)
    documento = models.CharField('Documento', max_length=35, null=True, blank=True)
    email = models.EmailField("Email", null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=20)

    def __str__(self):
        return self.nome
