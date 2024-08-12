from django import template
import locale

register = template.Library()


@register.filter
def methods(value):
    if value == 'CARTAO':
        return f'''
           <p class="card-text">Parcelas: {{payment.qt_parcelas}}</p>
           <p class="card-text">Valor Parcelas: {{payment.valor_parcelas}}</p>
        '''

