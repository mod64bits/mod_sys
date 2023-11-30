from django.urls import path
from .views import (ListaFornecedorView, NovoFornecedorView, EditarFornecedorView, DeletarFornecedorView,
                    ListaCategoriasView, NovaCategoriaView, EditarCategoriaView, DeletarCategoriaView
                    )

app_name = 'produtos'

urlpatterns = [
    path('fornecedores/', ListaFornecedorView.as_view(), name='lista_fornecedores'),
    path('fornecedor/novo/', NovoFornecedorView.as_view(), name='novo_fornecedor'),
    path('fornecedor/editar/<uuid:pk>/', EditarFornecedorView.as_view(), name="editar_fornecedor"),
    path('fornecedor/deletar/<uuid:pk>/', DeletarFornecedorView.as_view(), name='deletar_fornecedor'),
    # Categoria
    path('categorias/', ListaCategoriasView.as_view(), name='lista_categorias'),
    path('categoria/nova/', NovaCategoriaView.as_view(), name='nova_categoria'),
    path('categoria/editar/<uuid:pk>/', EditarCategoriaView.as_view(), name="editar_categoria"),
    path('categoria/deletar/<uuid:pk>/', DeletarCategoriaView.as_view(), name='deletar_categoria'),
]
