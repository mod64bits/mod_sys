from django.db import models
from apps.base.models import BaseModel


class Fornecedor(BaseModel):
    nome = models.CharField('Nome', max_length=50)
    cnpj = models.CharField('E-mail', max_length=50, null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=30, null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)

    class Meta:
        verbose_name = 'Fornecedo'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']


class Categoria(BaseModel):
    nome = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Fabricante(BaseModel):
    nome = models.CharField("Nome", max_length=50)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Frabricantes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(BaseModel):
    nome = models.CharField("Nome", max_length=150)
    fabricante = models.ForeignKey(
        Fabricante,
        on_delete=models.SET_NULL,
        verbose_name="Fabricante",
        related_name="produto_fabricante",
        null=True,
        blank=True
    )
    codigo = models.CharField("Codigo", max_length=0, null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        verbose_name='Categoria',
        related_name='p_categoria'
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        verbose_name='Fornecedor',
        related_name='p_fornecedor'
    )
    preco_compra = models.DecimalField('Preço de Compra', decimal_places=2, max_digits=8)

    def __str__(self):
        return f"{self.nome} --{self.preco_compra}"
