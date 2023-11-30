from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Fornecedor


class NovoFornecedorForm(BSModalModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"


