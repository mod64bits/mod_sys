from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Fornecedor, Categoria, Fabricante


class NovoFornecedorForm(BSModalModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"


class NovaCategoriaForm(BSModalModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"


class NovoFabricanteForm(BSModalModelForm):
    class Meta:
        model = Fabricante
        fields = "__all__"
