from django import template
import locale

register = template.Library()


@register.filter
def convert_real_br(value):
    if not value:
        value = 0
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    total = locale.currency(value, grouping=True, symbol=True)
    return total


@register.filter
def lucro(compra, venda):
    lucro = venda - compra
    _porcentagem = ((venda - compra) * 100) / compra
    porcentagem = "{:.2f}".format(_porcentagem)

    return f'''
    {lucro} <br/><span class="badge bg-warning">{porcentagem}%</span>'''
