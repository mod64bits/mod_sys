import decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .forms import PaymentForm
from .models import Payment
from django.db.models import signals

from apps.orcamentos.models import Orcamento
from apps.core.calculos import valor_porcentagem, desconto_avista


class AdcionarPagamentoOrcamentoView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payment/adcionar_pagamento_orcamento.html"

    def form_valid(self, form):
        payment_instance = form.save(commit=False)
        orcamento = Orcamento.objects.get(id=self.kwargs['pk'])
        payment_instance.orcamento = orcamento
        if form.is_valid():
            payment_instance.save()
            return HttpResponseRedirect(reverse_lazy('orcamentos:orcamento', args=[orcamento.pk]))




class EditarPagamentoOrcamentoView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payment/adcionar_pagamento_orcamento.html"

class DeletarPagamentoOrcamentoView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = "payment/payment_model_confirm_delete.html"
    def get_success_url(self):
        obj = self.get_object()
        return reverse_lazy('orcamentos:orcamento', args=[obj.orcamento.id])


def update_total_payment(sender, instance, signal, *args, **kwargs):
    total = instance.orcamento.total

    if instance.forma_pagamento == 'AVISTA' and instance.desconto > 0:
        descontos = desconto_avista(total, instance.desconto)
        instance.valor_desconto = descontos["desconto"]
        instance.total_desconto = descontos["valor_final"]
        total = descontos['valor_final']

    instance.valor_bruto =  instance.orcamento.total
    if instance.valor_entrada != decimal.Decimal('0.00') or None == instance.valor_entrada:
        if not  instance.valor_entrada:
            instance.valor_entrada = decimal.Decimal('0.00')
        valor_com_entrada =  instance.orcamento.total -  instance.valor_entrada
        obj_valores = valor_porcentagem(instance.acrecimo, valor_com_entrada)

    else:
        obj_valores = valor_porcentagem(instance.acrecimo, total)

    acrecimo = obj_valores['aumento']
    total_acrecimo = decimal.Decimal(obj_valores['total'])


    if instance.qt_parcelas > 1:
        instance.valor_parcelas = obj_valores['total'] / instance.qt_parcelas
    else:
        instance.valor_parcelas = obj_valores['total']

    instance.total= decimal.Decimal(total_acrecimo)
    instance.valor_acrecimo = decimal.Decimal(acrecimo)
    # if instance.forma_pagamento == 'AVISTA':
    #     instance.valor_entrada = total


signals.pre_save.connect(update_total_payment, sender=Payment)