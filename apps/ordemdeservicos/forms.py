import formset
from django.forms import fields, forms
from django.forms import ModelForm

from formset.widgets import DatePicker, DateTimePicker, DateTimeInput
from .models import OrdemDeServico


class OrdemServicoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['emissao'] = fields.DateTimeField(
            widget=DateTimeInput(),
        )

    class Meta:
        model = OrdemDeServico
        fields = ['prioridade', 'solicitante', 'responsavel', 'emissao', 'cliente', 'descricao']

