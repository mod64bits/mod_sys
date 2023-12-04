from .models import Servico, CategoriaServico
from bootstrap_modal_forms.forms import BSModalModelForm


class ServicoForm(BSModalModelForm):
    class Meta:
        model = Servico
        fields = '__all__'


class CategoriaServicoForm(BSModalModelForm):
    class Meta:
        model = CategoriaServico
        fields = '__all__'

