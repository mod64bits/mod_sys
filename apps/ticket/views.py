from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalUpdateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Ticket
from .forms import IniciarAtendimentoForm

class ListaDeTickets(ListView):
    template_name = "ticket/lista_ticket.html"

    def get_queryset(self):
        return Ticket.objects.extra(where=['status == ("ABERTO") OR status == ("EM_ATENDIMENTO") '])


class IniciarAtendimentoView(LoginRequiredMixin, BSModalUpdateView):
    model = Ticket
    form_class = IniciarAtendimentoForm
    template_name = 'ticket/iniciar_atendimento.html'
    success_message = 'Success: Cliente was deleted.'
    success_url = reverse_lazy('tickets:lista_tickets')

    def form_valid(self, form):
        form.instance.iniciado_em = datetime.now()
        form.instance.status = "EM_ATENDIMENTO"

        return super(IniciarAtendimentoView, self).form_valid(form)