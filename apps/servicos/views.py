from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Servico, CategoriaServico
from .forms import ServicoForm, CategoriaServicoForm

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalReadView
)


class ListaServicosView(LoginRequiredMixin, ListView):
    model = Servico
    template_name = 'servicos/servico_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_menu_servico'] = True
        context['open_menu_servico'] = True
        context['active_servico'] = True
        return context


class NovoServicoView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'servicos/novo_servico.html'
    form_class = ServicoForm
    success_message = 'Success:Servico Criado.'
    success_url = reverse_lazy('servicos:lista_servicos')


class EditarServicoView(LoginRequiredMixin, BSModalUpdateView):
    model = Servico
    template_name = 'servicos/editar_servico.html'
    form_class = ServicoForm
    success_message = 'Success: Serviço Atualizado.'
    success_url = reverse_lazy('servicos:lista_servicos')


class DeletarServicoView(LoginRequiredMixin, BSModalDeleteView):
    model = Servico
    template_name = 'servicos/deletar_servico.html'
    success_message = 'Success: Fornecedor excluído com sucesso.'
    success_url = reverse_lazy('servicos:lista_servicos')


class ListaCategoriaServicoView(LoginRequiredMixin, ListView):
    model = CategoriaServico
    template_name = 'servicos/lista_categoria_servico.html'


class NovaCategoriaServicoView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'servicos/nova_categoria_servico.html'
    form_class = CategoriaServicoForm
    success_message = 'Success: Tipo de Serviço Criado.'
    success_url = reverse_lazy('servicos:lista_categoria_servicos')


class EditarCategoriaServicoView(LoginRequiredMixin, BSModalUpdateView):
    model = CategoriaServico
    template_name = 'servicos/nova_categoria_servico.html'
    form_class = CategoriaServicoForm
    success_message = 'Success: Tipo Servico Atualizado.'
    success_url = reverse_lazy('servicos:lista_categoria_servicos')


class DeletarCategoriaServicoView(LoginRequiredMixin, BSModalDeleteView):
    model = CategoriaServico
    template_name = 'servicos/deletar_categoria_servico.html'
    success_message = 'Success: Tipo de servico excluído com sucesso.'
    success_url = reverse_lazy('servicos:lista_categoria_servicos')
