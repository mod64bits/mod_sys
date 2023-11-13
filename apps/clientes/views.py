from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .forms import ClienteForm
from .models import Cliente


class ListaClientesView(ListView):
    model = Cliente
    template_name = 'clientes/lista_clientes.html'


class NovoClienteView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'clientes/novo_cliente.html'
    form_class = ClienteForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('clientes:lista_cliente')
