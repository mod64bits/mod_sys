from django.urls import path
from .views import (ListaFornecedorView, NovoFornecedorView, EditarFornecedorView, DeletarFornecedorView,
                    ListaCategoriasView, NovaCategoriaView, EditarCategoriaView, DeletarCategoriaView,
                    ListaFabricantesView, NovoFabricanteView, EditarFabricanteView, DeletarFabricanteView,
                    ListaProdutosView, NovoProdutoView, EditarProdutoView
                    )

app_name = 'produtos'

urlpatterns = [
    path('', ListaProdutosView.as_view(), name='lista_produtos'),
    path('novo/', NovoProdutoView.as_view(), name='novo_produto'),
    path('editar/<uuid:pk>/', EditarProdutoView.as_view(), name='editar_produto'),
    # Produtos
    path('', ListaFornecedorView.as_view(), name='lista_fornecedores'),
    # Fornecedores
    path('fornecedores/', ListaFornecedorView.as_view(), name='lista_fornecedores'),
    path('fornecedor/novo/', NovoFornecedorView.as_view(), name='novo_fornecedor'),
    path('fornecedor/editar/<uuid:pk>/', EditarFornecedorView.as_view(), name="editar_fornecedor"),
    path('fornecedor/deletar/<uuid:pk>/', DeletarFornecedorView.as_view(), name='deletar_fornecedor'),
    # Categoria
    path('categorias/', ListaCategoriasView.as_view(), name='lista_categorias'),
    path('categoria/nova/', NovaCategoriaView.as_view(), name='nova_categoria'),
    path('categoria/editar/<uuid:pk>/', EditarCategoriaView.as_view(), name="editar_categoria"),
    path('categoria/deletar/<uuid:pk>/', DeletarCategoriaView.as_view(), name='deletar_categoria'),
    # Fabricantes
    path('fabrincates/', ListaFabricantesView.as_view(), name='lista_fabricantes'),
    path('fabrincate/nova/', NovoFabricanteView.as_view(), name='novo_fabricante'),
    path('fabrincate/editar/<uuid:pk>/', EditarFabricanteView.as_view(), name='editar_fabricante'),
    path('fabrincate/deletar/<uuid:pk>/', DeletarFabricanteView.as_view(), name='deletar_fabricante'),
]
