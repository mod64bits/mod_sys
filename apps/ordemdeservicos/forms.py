from ckeditor.widgets import CKEditorWidget
from django import forms
from apps.core.ultils import gerador_de_codigo
from formset.widgets import DatePicker, DateTimePicker, DateTimeInput
from .models import OrdemDeServico, ItemOS
from bootstrap_modal_forms.forms import BSModalModelForm

class OrdemServicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['emissao'] = forms.fields.DateTimeField(
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

class EditarOrdemServicoForm(BSModalModelForm):
    resolucao = forms.CharField(widget=CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super(EditarOrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['inicio_execucao'] = forms.fields.DateTimeField(
            widget=DateTimeInput(),
        )
        self.fields['fim_execucao'] = forms.fields.DateTimeField(
            widget=DateTimeInput(),
        )
    class Meta:
        model = OrdemDeServico
        fields = ['prioridade', 'responsavel', 'status', 'inicio_execucao', 'resolucao', 'fim_execucao', 'total_equipamentos', 'total']


class EditarOrdemCompletaForm(forms.ModelForm):
    descricao = forms.CharField(widget=CKEditorWidget())
    resolucao = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super(EditarOrdemCompletaForm, self).__init__(*args, **kwargs)
        self.fields['inicio_execucao'] = forms.fields.DateTimeField(
            widget=DateTimeInput(),
        )
        self.fields['fim_execucao'] = forms.fields.DateTimeField(
            widget=DateTimeInput(),
        )

    class Meta:
        model = OrdemDeServico
        fields = '__all__'

class AdcionarItemForm(BSModalModelForm):
    class Meta:
        model = ItemOS
        fields = '__all__'


    # def save(self, commit=True):
    #     instance = super(AdcionarItemForm, self).save(commit=False)
    #     instance.total = instance.preco * instance.quantidade
    #     if commit:
    #         instance.save()
    #     return instance
