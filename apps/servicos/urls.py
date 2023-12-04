from django.urls import path
from .views import (ListaServicosView, NovoServicoView, DeletarServicoView, EditarServicoView, ListaCategoriaServicoView,
                    NovaCategoriaServicoView, EditarCategoriaServicoView, DeletarCategoriaServicoView
                    )

app_name = 'servicos'

urlpatterns = [
    path('', ListaServicosView.as_view(), name='lista_servicos'),
    path('novo/', NovoServicoView.as_view(), name='novo_servico'),
    path('editar/<uuid:pk>/', EditarServicoView.as_view(), name='editar_servico'),
    path('deletar/<uuid:pk>/', DeletarServicoView.as_view(), name='deletar_servico'),
    # Categoria
    path('categorias/', ListaCategoriaServicoView.as_view(), name='lista_categoria_servicos'),
    path('categoria/novo/', NovaCategoriaServicoView.as_view(), name='novo_categoria_servico'),
    path('categoria/editar/<uuid:pk>/', EditarCategoriaServicoView.as_view(), name='editar_categoria_servico'),
    path('categoria/deletar/<uuid:pk>/', DeletarCategoriaServicoView.as_view(), name='deletar_categoria_servico'),

]
