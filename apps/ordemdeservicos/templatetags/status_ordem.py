from django import template


register = template.Library()


@register.filter
def ordem_status(value):
    status = ""
    if value == 0:
        status = "<span class='badge bg-danger'>Não Execultado</span>"
        return status
    if value == 1:
        status = "<span class='badge bg-warning'>Em Execução</span>"
        return status


