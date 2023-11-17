from django.views.generic.list import ListView
from .models import Ticket


class ListaDeTickets(ListView):
    template_name = "ticket/lista_ticket.html"

    def get_queryset(self):
        return Ticket.objects.extra(where=['status == ("ABERTO") OR status == ("EM_ATENDIMENTO") '])

