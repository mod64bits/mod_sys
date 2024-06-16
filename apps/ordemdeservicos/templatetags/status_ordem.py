from django import template


register = template.Library()


@register.filter
def ordem_status(value):
    if value == 0:
        status = "<span class='badge bg-danger '>Não Execultado</span>"
        return status
    if value == 1:
        status = "<span class='badge bg-info '>Em Execução</span>"
        return status
    if value == 2:
        status = "<span class='badge bg-success '>Finalizado</span>"
        return status
    if value == 3:
        status = "<span class='badge bg-warning'>Aguardando Equipamento(s)</span>"
        return status


