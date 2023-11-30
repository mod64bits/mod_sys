from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Fornecedor, Categoria


class NovoFornecedorForm(BSModalModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"


class NovaCategoriaForm(BSModalModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"
