from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.base.models import BaseModel
from apps.clientes.models import Cliente
from apps.produtos.models import Produto
from apps.servicos.models import Servico
from apps.core.ultils import Datas


class Orcamento(BaseModel):
    STATUS_CHOICES = (
        (0, 'Não Enviado'),
        (1, 'Em Analise'),
        (2, 'Aprovado'),
        (3, 'Cancelada'),
        (4, 'Regeitado'),
    )
    validade = models.DateField('Validade', default=Datas().vencimento())
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        verbose_name='Cliente',
        related_name='orcamento_cliente'
    )
    total = models.DecimalField('Total', decimal_places=2, max_digits=8, null=True, blank=True)
    total_equipamentos = models.DecimalField('Total Equipamentos', decimal_places=2, max_digits=8, null=True,
                                             blank=True)
    total_mao_de_obra = models.DecimalField('Total Mão de Obra', decimal_places=2, max_digits=8, null=True, blank=True)
    total_lucro = models.DecimalField('Total Lucro', decimal_places=2, max_digits=8, null=True, blank=True)
    total_compra = models.DecimalField('Total Compra', decimal_places=2, max_digits=8, null=True, blank=True)
    descricao = models.TextField("Descrição", null=True, blank=True)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return f"{self.cliente.nome}"

    def get_absolute_url(self):
        return reverse('orcamentos:orcamento', kwargs={'pk': self.id})


class ItemProduto(BaseModel):
    orcamento = models.ForeignKey(
        Orcamento,
        on_delete=models.CASCADE,
        verbose_name='Orcamento',
        related_name='produto_orcamento'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name='Produto',
        related_name='item_produto',
    )
    porcentagem = models.DecimalField('Porcentagem', max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    preco = models.DecimalField("Preço de Compra", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total = models.DecimalField("Total", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Item Produto'
        verbose_name_plural = 'itens Produtos'
        ordering = ['-created']

    def __str__(self):
        return f"{self.produto}  -  {self.preco}"

    def get_absolute_url(self):
        return reverse('orcamentos:orcamento', kwargs={'pk': self.orcamento.id})


class ItemMaoDeObra(BaseModel):
    orcamento = models.ForeignKey(
        Orcamento,
        on_delete=models.CASCADE,
        verbose_name='Orçamento',
        related_name='mao_obra_orcamento'
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        verbose_name='Serviço',
        related_name='item_servico'
    )
    descricao = models.TextField('Descrição', null=True, blank=True)
    valor = models.DecimalField("Preço", max_digits=16, decimal_places=2, null=True, blank=True, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    total = models.DecimalField("Total", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Item Serviço'
        verbose_name_plural = 'Itens Serviços'
        ordering = ['-created']

    def __str__(self):
        return f"{self.servico} - {self.valor}"

    def get_absolute_url(self):
        return reverse('orcamento:update_orcamento', kwargs={'pk': self.orcamento.id})


class InformacoesOrcamento(BaseModel):
    orcamento = models.OneToOneField(
        Orcamento,
        on_delete=models.PROTECT,
        verbose_name='Descricao'
    )
    titulo = models.CharField("Descrição")
    descricao = models.TextField('Descrição', null=True, blank=True)

    def __str__(self):
        return self.titulo
