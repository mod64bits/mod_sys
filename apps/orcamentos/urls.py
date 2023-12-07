from django.urls import path
from .views import ListaOrcamentoView, NovoOrcamentoView, OrcamentoView

app_name = 'orcamentos'


urlpatterns = [
    path('', ListaOrcamentoView.as_view(), name='lista_orcamento'),
    path('novo/', NovoOrcamentoView.as_view(), name='novo_orcamento'),
    path('<uuid:pk>/', OrcamentoView.as_view(), name='orcamento'),
]