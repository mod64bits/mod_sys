from django.db import models
from apps.base.models import BaseModel


class CategoriaServico(BaseModel):
    nome = models.CharField("Nome", max_length=100, unique=True)

    class Meta:
        verbose_name = 'Categoria Serviço'
        verbose_name_plural = 'Categorias Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Servico(BaseModel):
    categoria_servico = models.ForeignKey(
        CategoriaServico, on_delete=models.CASCADE,
        verbose_name='Serviço',
        related_name='categoria_servico'
    )
    nome = models.CharField('Nome', max_length=100)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Serviços'
        verbose_name_plural = 'Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome
