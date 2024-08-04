from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Payment



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['forma_pagamento', 'qt_parcelas', 'acrecimo', 'valor_entrada']