from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.users.models import User
from apps.base.models import BaseModel
from apps.clientes.models import Cliente
from apps.produtos.models import Produto


class OrdemDeServico(BaseModel):
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
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name='Produto',
        related_name='os_produto',
    )
    quantidade = models.PositiveIntegerField('Quantidade', default=1)
    porcentagem = models.DecimalField('Porcentagem', max_digits=16, null=True, blank=True, decimal_places=2,
                                      validators=[
                                          MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    preco = models.DecimalField("Preço de Compra", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    total = models.DecimalField("Total", max_digits=16, null=True, blank=True, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self) -> str:
        return f"{self.ordem_servico.descricao}-{self.produto.nome}"
