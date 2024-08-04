import decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from .forms import PaymentForm
from .models import Payment
from django.db.models import signals

from apps.orcamentos.models import Orcamento
from apps.core.calculos import valor_porcentagem

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


def update_total_payment(sender, instance, signal, *args, **kwargs):
    obj_valores = valor_porcentagem(instance.acrecimo, instance.orcamento.total)
    acrecimo = obj_valores['aumento']
    total_acrecimo = decimal.Decimal(obj_valores['total'])
    instance.total_acrecimo =  decimal.Decimal(total_acrecimo)
    instance.valor_acrecimo =  decimal.Decimal(acrecimo)
    instance.valor_bruto =  instance.orcamento.total


signals.pre_save.connect(update_total_payment, sender=Payment)