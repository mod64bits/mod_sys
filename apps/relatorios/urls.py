from django.urls import path

from .views import (OrcamentoSimples
                    )

app_name = 'relatorios'

urlpatterns = [
    path('impreimir/orcamento/simples/<uuid:pk>/', OrcamentoSimples.as_view(), name='orcamento_simples'),
]
