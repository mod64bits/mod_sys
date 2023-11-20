from .models import Ticket
from bootstrap_modal_forms.forms import BSModalModelForm


class IniciarAtendimentoForm(BSModalModelForm):
    class Meta:
        model = Ticket
        fields = ["responsavel"]


