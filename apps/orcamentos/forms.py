from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import InformacoesOrcamento, Orcamento


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
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            )
        }