from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import User
from apps.base.models import BaseModel
from apps.clientes.models import Cliente
from apps.produtos.models import Produto
from django.urls import reverse

class OrdemDeServico(BaseModel):
    PRIORIDADE_CHOICES = (
        ("BAIXA", "BAIXA"),
        ("MEDIA", "MEDIA"),
        ("ALTA", "ALTA"),
        ("URGENTE", "URGENTE"),
    )
    STATUS_CHOICES = (
        (0, "Não Execultado"),
        (1, "Em Execução"),
        (2, "Finalizado"),
        (3, "Aguardando Equipamento(s)"),
    )
    solicitante = models.CharField('Solicitante', max_length=150, null=True, blank=True)
    responsavel = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Responsavel",
        related_name="os_user"
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0)
    prioridade = models.CharField("Prioridade", choices=PRIORIDADE_CHOICES, default= "BAIXA", max_length=15, null=True, blank=True)
    codigo = models.CharField("Código", max_length=100, null=True, blank=True, editable=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="os_cliente"
    )
    emissao = models.DateTimeField("Emissao", null=True, blank=True)
    inicio_execucao = models.DateTimeField("Inicio", null=True, blank=True)
    descricao = models.TextField("Descrição da OS")
    resolucao = models.TextField("Resolução", null=True, blank=True)

    fim_execucao = models.DateTimeField('Fechamento', null=True, blank=True)
    tempo_total = models.CharField('Tempo Total', null=True, blank=True, editable=False)
    tempo_servico = models.CharField('Tempo Servico', null=True, blank=True, editable=False)
    total = models.DecimalField("Total", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    total_equipamentos = models.DecimalField("Total Equipamentos", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self) -> str:
        return self.descricao




class ItemOS(BaseModel):
    ordem_servico = models.ForeignKey(
        OrdemDeServico,
        on_delete=models.CASCADE,
        verbose_name='OS',
        related_name='produto_OS'
    )
    item = models.CharField('Item', max_length=150, null=True, blank=True)
    quantidade = models.PositiveIntegerField('Quantidade', default=1)

    preco = models.DecimalField("Preço de Compra", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total = models.DecimalField("Total", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self) -> str:
        return f"{self.ordem_servico.descricao}-{self.item}"



def update_total_item_ordem(sender, instance, signal, *args, **kwargs):
    ordem = instance.ordem_servico
    total_item = 0
    preco = 0


    obj = ItemOS.objects.filter(ordem_servico=ordem)

    for item in obj:
        if not item.total:
            continue
        total_item += item.total
    for product in obj:
        total_item = ordem.preco * product.quantidade


    _obj_produto_compra = ItemProduto.objects.filter(orcamento=orcamento)
    _obj_compra_mao_de_obra = ItemMaoDeObra.objects.filter(orcamento=orcamento)
    tota_item_compra = 0
    for item_comp in _obj_produto_compra:
        tota_item_compra += item_comp.produto.preco_compra * item_comp.quantidade

    orcamento.total_equipamentos = total_produtos
    orcamento.total_mao_de_obra = total_mao_de_obra
    orcamento.total = total_produtos + total_mao_de_obra

    orcamento.total_compra = total_compra

    orcamento.total_lucro = ((total_produtos + total_mao_de_obra) - tota_item_compra)

    orcamento.save()