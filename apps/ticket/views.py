from datetime import datetime
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalUpdateView
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from apps.ticket.models import IamagemAtendimento
from .serializer import UploadImagemAtendimentoSerializer
from .models import Ticket, Atendimento, MensagemAtendimento
from .forms import IniciarAtendimentoForm
from django.views.generic.base import RedirectView, View

from ..core.ultils import gerar_protocolo
from django.http import HttpResponse, JsonResponse

class ListaDeTickets(ListView):
    model = Ticket
    template_name = "ticket/lista_ticket.html"

    # def get_queryset(self):
    #     return Ticket.objects.extra(where=['status == ("ABERTO") OR status == ("EM_ATENDIMENTO") '])



class IniciarAtendimentoView(LoginRequiredMixin, BSModalUpdateView):
    model = Ticket
    form_class = IniciarAtendimentoForm
    template_name = 'ticket/iniciar_atendimento.html'
    success_message = 'Success: Cliente was deleted.'
    # success_url = reverse_lazy('tickets:lista_tickets')

    def get_success_url(self):
        return reverse('tickets:atendimento', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.iniciado_em = datetime.now()
        form.instance.status = "EM_ATENDIMENTO"
        return super(IniciarAtendimentoView, self).form_valid(form)


class AtendimentoRedirect(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        if Atendimento.objects.filter(ticket=ticket).exists():
            atendimento = Atendimento.objects.get(ticket=ticket)
            return reverse('tickets:atendimento', kwargs={'pk': atendimento.pk})

        atendimento_obj = Atendimento.objects.create(
            protocolo=gerar_protocolo(),
            ticket=ticket
        )
        MensagemAtendimento.objects.create(
            atendimento=atendimento_obj,
            atendente=ticket.responsavel,
            mensagem="Olá, Estaremos dando Inicio ao seu atendimento"
        )
        return reverse('tickets:atendimento', args=[atendimento_obj.pk])


class AtendimentoView(DetailView):
    model = Atendimento
    template_name = "ticket/atendimento.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context["mensagens"] = obj.atendimento_mensagem.all()
        return context


class UploadImagemViwSet(viewsets.ModelViewSet):
    queryset = IamagemAtendimento.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadImagemAtendimentoSerializer

    def perform_create(self, serializer):
        print()
        atendimento = Atendimento.objects.get(id=self.kwargs['pk'])
        serializer.save(atendimento=atendimento)


class UploadFile(View):
    def post(self, request, *args, **kwargs):
        my_file = request.FILES.get('file')
        _atendimento = Atendimento.objects.get(id=kwargs["pk"])
        IamagemAtendimento.objects.create(
            atendimento=_atendimento,
            imagem=my_file
        )
        return HttpResponse('')