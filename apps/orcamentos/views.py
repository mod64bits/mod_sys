import decimal
from django.db.models import signals
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from .models import Orcamento, ItemProduto, ItemMaoDeObra
from .forms import (NovoOrcamentoForm, OrcamentoItemProdutoForm, OrcamentoItemServico, GerarOrcamentoForm,
                    EditarDescricaoOrcamentoForm)
from django.views.generic.edit import CreateView


class ListaOrcamentoView(LoginRequiredMixin, ListView):
    model = Orcamento
    template_name = 'orcamentos/lista_orcamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_open_orcamento'] = True
        context['active_orcamentos'] = True
        return context


class NovoOrcamentoView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'orcamentos/novo_orcamento.html'
    form_class = NovoOrcamentoForm

    success_message = 'Success: Cliente was created.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('orcamentos:orcamento', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return super(NovoOrcamentoView, self).form_valid(form)


class OrcamentoView(LoginRequiredMixin, TemplateView):
    template_name = 'orcamentos/orcamento.html'

    # def get(self, request, *args, **kwargs):
    #     orcamento = Orcamento.objects.get(id=kwargs['pk'])
    #
    #     return super(OrcamentoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orcamento'] = Orcamento.objects.get(id=kwargs['pk'])
        context['qt_produtos'] = self.quantidade_itens
        context['lucro_equipamentos'] = self.total_lucro_equipamentos(context['orcamento'].total_equipamentos,
                                                                      context['orcamento'].total_compra)
        return context

    def total_lucro_equipamentos(self, total_equipamentos, total_compra):
        equipamentos_compra = total_compra if total_compra else Decimal(0.00)
        equipamentos_venda = total_equipamentos if total_equipamentos else Decimal(0.00)

        return Decimal(equipamentos_venda - equipamentos_compra)

    @property
    def quantidade_itens(self):
        obj = ItemProduto.objects.filter(orcamento_id=self.kwargs['pk'])
        qt_total_itens = 0
        qt_itens = len(obj)
        for item in obj:
            qt_total_itens += item.quantidade

        total = {
            "qt_intens": qt_itens,
            "qt_total_itens": qt_total_itens
        }
        return total


class AdcionarProdutoView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'orcamentos/adcionar_item.html'
    form_class = OrcamentoItemProdutoForm
    success_message = 'Success: Book was created.'

    def form_valid(self, form):
        self.orcamento = Orcamento.objects.get(id=self.kwargs['pk'])
        qt = form.instance.quantidade
        percent = decimal.Decimal(form.instance.porcentagem)
        if ItemProduto.objects.filter(produto_id=form.instance.produto.id, orcamento=self.orcamento).exists():
            produto = ItemProduto.objects.get(produto_id=form.instance.produto.id, orcamento=self.orcamento)
            form.instance = produto
            form.instance.quantidade += qt
        form.instance.orcamento = self.orcamento
        form.instance.porcentagem = percent
        form.instance.preco = decimal.Decimal(self.valor_porcentagem(percent, form.instance.produto.preco_compra))

        form.instance.total = decimal.Decimal(form.instance.preco * form.instance.quantidade)

        return super(AdcionarProdutoView, self).form_valid(form)

    def valor_porcentagem(self, percentual, valor_compra):
        _percentual = percentual / decimal.Decimal(100)
        aumento = decimal.Decimal(_percentual) * valor_compra
        total = decimal.Decimal(valor_compra + aumento)

        return total

    def get_success_url(self, **kwargs):
        return reverse_lazy('orcamentos:orcamento', kwargs={'pk': self.orcamento.pk})


class EditarProdutoView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemProduto
    template_name = 'orcamentos/adcionar_item.html'
    form_class = OrcamentoItemProdutoForm

    def form_valid(self, form):
        percent = decimal.Decimal(form.instance.porcentagem)
        place_product = decimal.Decimal(form.instance.produto.preco_compra)
        form.instance.preco = decimal.Decimal(self.valor_porcentagem(percent, place_product))
        form.instance.total = decimal.Decimal(form.instance.preco * form.instance.quantidade)
        return super(EditarProdutoView, self).form_valid(form)

    def valor_porcentagem(self, percentual, valor_compra):
        _percentual = percentual / decimal.Decimal(100)
        aumento = decimal.Decimal(_percentual) * valor_compra
        total = decimal.Decimal(valor_compra + aumento)
        return total


class DeleteItemView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemProduto
    template_name = 'orcamentos/delete_item.html'
    success_message = 'Success: Categoria excluída com sucesso.'

    def get_success_url(self):
        orcamento = self.get_object()
        return reverse('orcamentos:orcamento', kwargs={'pk': orcamento.orcamento.id})


class VerInforProdutoView(LoginRequiredMixin, BSModalReadView):
    model = ItemProduto
    template_name = 'orcamentos/ver_informacoes_produto.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_und'] = obj.preco - obj.produto.preco_compra
        context['l_total'] = (obj.preco - obj.produto.preco_compra) * obj.quantidade

        return context

    def valor_porcentagem(self, percentual, valor_compra):
        _percentual = percentual / decimal.Decimal(100)
        aumento = decimal.Decimal(_percentual) * valor_compra
        total = decimal.Decimal(valor_compra + aumento)
        return total


class AdicionarItemServicoView(LoginRequiredMixin, BSModalCreateView):
    model = ItemMaoDeObra
    template_name = 'orcamentos/adcionar_item_servico.html'
    form_class = OrcamentoItemServico

    def form_valid(self, form):
        self.orcamento = Orcamento.objects.get(id=self.kwargs['pk'])
        qt = form.instance.quantidade

        if ItemMaoDeObra.objects.filter(servico_id=form.instance.id).exists():
            servico = ItemMaoDeObra.objects.get(produto_id=form.instance.id, orcamento=self.orcamento)
            form.instance = servico
            form.instance.quantidade += qt
        form.instance.orcamento = self.orcamento

        form.instance.total = decimal.Decimal(form.instance.valor * form.instance.quantidade)

        return super(AdicionarItemServicoView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('orcamentos:orcamento', kwargs={'pk': self.orcamento.pk})


class EditarItemServicoView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemMaoDeObra
    template_name = 'orcamentos/adcionar_item_servico.html'
    form_class = OrcamentoItemServico

    def form_valid(self, form):
        self.orcamento = self.object.orcamento
        form.instance.total = decimal.Decimal(form.instance.valor * form.instance.quantidade)
        return super(EditarItemServicoView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('orcamentos:orcamento', kwargs={'pk': self.orcamento.pk})


class InformacoesServicosView(LoginRequiredMixin, BSModalReadView):
    model = ItemMaoDeObra
    template_name = 'orcamentos/informacoes_servicos.html'


class DeleteServicoView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemMaoDeObra
    template_name = 'orcamentos/delete_servico.html'
    success_message = 'Success: Categoria excluída com sucesso.'

    def get_success_url(self):
        orcamento = self.get_object()
        return reverse('orcamentos:orcamento', kwargs={'pk': orcamento.orcamento.id})


class GerarOrcamentoView(LoginRequiredMixin, CreateView):
    form_class = GerarOrcamentoForm
    template_name = 'orcamentos/gerar_orcamento.html'


class EditarDescricaoOrcamentoView(LoginRequiredMixin, UpdateView):
    model = Orcamento
    form_class = EditarDescricaoOrcamentoForm
    template_name = 'orcamentos/editar_descricao_orcamento.html'


def update_total_orcamento(sender, instance, signal, *args, **kwargs):
    orcamento = instance.orcamento
    total_produtos = 0
    total_mao_de_obra = 0
    total_compra = 0
    obj = ItemProduto.objects.filter(orcamento=orcamento)
    obj_mao_de_obra = ItemMaoDeObra.objects.filter(orcamento=orcamento)

    for produto_item in obj:
        if not produto_item.total:
            continue
        total_produtos += produto_item.total
    for product in obj:
        total_compra += product.produto.preco_compra * product.quantidade
    for item_servico in obj_mao_de_obra:
        if not item_servico.total:
            continue
        total_mao_de_obra += item_servico.total

    _obj_produto_compra = ItemProduto.objects.filter(orcamento=orcamento)
    _obj_compra_mao_de_obra = ItemMaoDeObra.objects.filter(orcamento=orcamento)
    tota_item_compra = 0
    for item_comp in _obj_produto_compra:
        tota_item_compra += item_comp.produto.preco_compra * item_comp.quantidade

    orcamento.total_equipamentos = total_produtos
    orcamento.total_mao_de_obra = total_mao_de_obra
    orcamento.total = total_produtos + total_mao_de_obra

    orcamento.total_compra = total_compra

    orcamento.total_lucro = ((total_produtos + total_mao_de_obra) - tota_item_compra)

    orcamento.save()


signals.post_save.connect(update_total_orcamento, sender=ItemProduto)
signals.post_delete.connect(update_total_orcamento, sender=ItemProduto)

signals.post_save.connect(update_total_orcamento, sender=ItemMaoDeObra)
signals.post_delete.connect(update_total_orcamento, sender=ItemMaoDeObra)
