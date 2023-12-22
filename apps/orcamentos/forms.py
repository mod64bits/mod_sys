from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
from .models import InformacoesOrcamento, Orcamento, ItemProduto, ItemMaoDeObra
from apps.clientes.models import Cliente


class NovoOrcamentoForm(BSModalModelForm):
    class Meta:
        model = Orcamento
        fields = ['cliente']


class InformacoesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["descricao"].required = False

    class Meta:
        model = InformacoesOrcamento
        fields = ("titulo", "descricao")


class OrcamentoItemProdutoForm(BSModalModelForm):
    class Meta:
        model = ItemProduto
        exclude = ['orcamento']


class OrcamentoItemServico(BSModalModelForm):
    descricao = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ItemMaoDeObra
        exclude = ['orcamento']


class GerarOrcamentoForm(forms.ModelForm):
    descricao = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Orcamento
        fields = ['cliente', 'descricao']
