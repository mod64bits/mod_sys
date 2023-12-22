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


@register.filter
def status(value):
    if value == 0:
        return f'''
            <small class="badge badge-info"><i class="far fa-clock"></i> Não Enviado</small>
        '''

    if value == 1:
        return f'''
            <small class="badge badge-warning"><i class="far fa-clock"></i> Em Analise</small>
        '''
    if value == 2:
        return f'''
           <small class="badge badge-warning"><i class="far fa-clock"></i> Cancelada</small>
        '''
    if value == 3:
        return f'''
              <small class="badge badge-secondary"><i class="far fa-clock"></i> 1 month</small>
           '''
    if value == 4:
        return f'''
           <small class="badge badge-danger"><i class="far fa-clock"></i> Regeitado</small>
        '''