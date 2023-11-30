from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from .models import Fornecedor, Categoria
from .forms import NovoFornecedorForm, NovaCategoriaForm


class ListaFornecedorView(LoginRequiredMixin, ListView):
    template_name = 'produtos/lista_fornecedores.html'

    def get_queryset(self):
        return Fornecedor.objects.all().order_by("nome")


class NovoFornecedorView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'produtos/novo_fornecedor.html'
    form_class = NovoFornecedorForm
    success_message = 'Success: Fornecedor Criado!'
    success_url = reverse_lazy('produtos:lista_fornecedores')


class EditarFornecedorView(LoginRequiredMixin, BSModalUpdateView):
    model = Fornecedor
    form_class = NovoFornecedorForm
    template_name = 'produtos/novo_fornecedor.html'
    success_url = reverse_lazy('produtos:lista_fornecedores')


class DeletarFornecedorView(LoginRequiredMixin, BSModalDeleteView):
    model = Fornecedor
    template_name = 'produtos/deletar_fornecedor.html'
    success_message = 'Success: Fornecedor Deletado!'
    success_url = reverse_lazy('produtos:lista_fornecedores')


# categorias

class ListaCategoriasView(LoginRequiredMixin, ListView):
    template_name = 'produtos/lista_categorias.html'

    def get_queryset(self):
        return Categoria.objects.all().order_by("nome")


class NovaCategoriaView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'produtos/nova_categoria.html'
    form_class = NovaCategoriaForm
    success_message = 'Success: Categoria Criado!'
    success_url = reverse_lazy('produtos:lista_categorias')


class EditarCategoriaView(LoginRequiredMixin, BSModalUpdateView):
    model = Categoria
    form_class = NovaCategoriaForm
    template_name = 'produtos/nova_categoria.html'
    success_url = reverse_lazy('produtos:lista_categorias')


class DeletarCategoriaView(LoginRequiredMixin, BSModalDeleteView):
    model = Categoria
    template_name = 'produtos/deletar_categoria.html'
    success_message = 'Success: Categoria Deletada!'
    success_url = reverse_lazy('produtos:lista_categorias')
