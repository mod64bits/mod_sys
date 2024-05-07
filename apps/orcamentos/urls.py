from django.urls import path
from .views import (ListaOrcamentoView, NovoOrcamentoView, OrcamentoView, AdcionarProdutoView, EditarProdutoView,
                    DeleteItemView, VerInforProdutoView, AdicionarItemServicoView, EditarItemServicoView,
                    InformacoesServicosView, DeleteServicoView, GerarOrcamentoView, EditarDescricaoOrcamentoView, MudarStausOrcamentoView)

app_name = 'orcamentos'


urlpatterns = [
    path('', ListaOrcamentoView.as_view(), name='lista_orcamento'),
    path('novo/', NovoOrcamentoView.as_view(), name='novo_orcamento'),
    path('<uuid:pk>/', OrcamentoView.as_view(), name='orcamento'),
     path('mudar/status/<uuid:pk>/', MudarStausOrcamentoView.as_view(), name='mudar_status'),
    # Item produto
    path('adcionar/produto/<uuid:pk>/', AdcionarProdutoView.as_view(), name='adcionar_produto_orcamento'),
    path('editar/produto/<uuid:pk>/', EditarProdutoView.as_view(), name='editar_produto_orcamento'),
    path('deletar/produto/<uuid:pk>/', DeleteItemView.as_view(), name='deletar_produto_orcamento'),
    path('informacoes/produto/<uuid:pk>/', VerInforProdutoView.as_view(), name='infor_produto_orcamento'),
    # Item serviços
    path('adcionar/servico/<uuid:pk>/', AdicionarItemServicoView.as_view(), name='adcionar_servico_orcamento'),
    path('editar/servico/<uuid:pk>/', EditarItemServicoView.as_view(), name='editar_servico_orcamento'),
    path('informacoes/servico/<uuid:pk>/', InformacoesServicosView.as_view(), name='infor_servico_orcamento'),
    path('deletar/servico/<uuid:pk>/', DeleteServicoView.as_view(), name='deletar_servico_orcamento'),

    path('gerar/', GerarOrcamentoView.as_view(), name='gerar_orcamento'),
    path('editar/descricao/<uuid:pk>/', EditarDescricaoOrcamentoView.as_view(), name='editar_descricao_orcamento'),
]