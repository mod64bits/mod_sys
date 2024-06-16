import formset
from django.forms import fields, forms
from django.forms import ModelForm
from apps.core.ultils import gerador_de_codigo
from formset.widgets import DatePicker, DateTimePicker, DateTimeInput
from .models import OrdemDeServico
from bootstrap_modal_forms.forms import BSModalModelForm

class OrdemServicoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['emissao'] = fields.DateTimeField(
            widget=DateTimeInput(),
        )

    class Meta:
        model = OrdemDeServico
        fields = ['prioridade', 'solicitante', 'responsavel', 'emissao', 'cliente', 'descricao']

    def save(self, commit=True):
        instance = super(OrdemServicoForm, self).save(commit=False)
        if not instance.codigo:
            instance.codigo = gerador_de_codigo(instance.cliente.nome)
        if commit:
            instance.save()
        return instance

class MudarStatusForm(BSModalModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['status']