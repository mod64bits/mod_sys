from django.db import models
from django.db.models import signals
from apps.base.models import BaseModel
from apps.clientes.models import Cliente
from apps.core.ultils import gerar_protocolo
from apps.users.models import User


class Ticket(BaseModel):
    STATUS = (
        ('ABERTO', 'ABERTO'),
        ('EM_ATENDIMENTO', 'EM ATENDIMENTO'),
        ('ENCERRADA', 'ENCERRADA'),
        ('CANCELADA', 'CANCELADA')
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name='CLIENTE',
        related_name='ticket_cliente',
        null=True,
        blank=True
    )
    solicitante = models.CharField('Solicitantes', max_length=100)
    departamento = models.CharField('Departamento', max_length=100)
    descricao = models.TextField("Descrição do chamado")
    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='responsible_tick',

    )
    iniciado_em = models.DateTimeField(null=True, blank=True)
    status = models.CharField("Status", max_length=15, choices=STATUS, default='ABERTO')
    fechado_em = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.solicitante


class Atendimento(BaseModel):
    protocolo = models.CharField("Protocolo", max_length=100, null=True, blank=True)
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.PROTECT,
        verbose_name="Ticket",
        related_name="atend_ticket",
    )

    def __str__(self):
        return self.protocolo


class MensagemAtendimento(BaseModel):
    atendimento = models.ForeignKey(
        Atendimento,
        verbose_name="Atendimento",
        related_name="atendimento_mensagem",
        on_delete=models.PROTECT
    )
    mensagem = models.TextField("Mensagem")
    cliente = models.ForeignKey(
        Cliente,
        verbose_name="Cliente",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    atendente = models.ForeignKey(
        User,
        verbose_name="Atendente",
        on_delete=models.CASCADE,
        related_name="user_mensagem",
        null=True,
        blank=True
    )
    arquivo = models.FileField("Arquivo", help_text="JPG, PDF, PNG", null=True, blank=True,
                               upload_to="atendimentos"
                               )

    def __str__(self):
        return self.atendimento


def criar_atendimento(sender, instance, signal, *args, **kwargs):
    if instance.status != "EM_ATENDIMENTO":
        return
    else:
        atendimento_obj = Atendimento.objects.create(
            protocolo=gerar_protocolo(),
            ticket=instance
        )
        MensagemAtendimento.objects.create(
            atendimento=atendimento_obj,
            atendente=instance.responsavel,
            mensagem="Olá, Estaremos dando Inicio ao seu atendimento"
        )


class IamagemAtendimento(BaseModel):
    atendimento = models.ForeignKey(
        Atendimento,
        verbose_name="Atendimento",
        related_name="img_atendimento",
        on_delete=models.CASCADE
    )
    imagem = models.ImageField("Imagem", upload_to="imagem/atendimentos")

    def __str__(self):
        return self.atendimento.protocolo