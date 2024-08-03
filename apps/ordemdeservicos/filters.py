import django_filters
from .models import OrdemDeServico


class OrdemStatusFilter(django_filters.FilterSet):
    FILTER_CHOICES = (
        (0, "Não Execultado"),
        (1, "Em Execução"),
        (2, "Finalizado"),
        (3, "Aguardando Equipamento(s)"),
)
    status = django_filters.ChoiceFilter(choices=FILTER_CHOICES)
    cliente = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = OrdemDeServico
        fields = ['status', 'cliente']