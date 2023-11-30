from django.urls import path
from .views import ListaFornecedorView, NovoFornecedorView, EditarFornecedorView, DeletarFornecedorView

app_name = 'produtos'


urlpatterns = [
    path('fornecedores/', ListaFornecedorView.as_view(), name='lista_fornecedores'),
    path('fornecedor/novo/', NovoFornecedorView.as_view(), name='novo_fornecedor'),
    path('fornecedor/editar/<uuid:pk>/', EditarFornecedorView.as_view(), name="editar_fornecedor"),
    path('fornecedor/deletar/<uuid:pk>/', DeletarFornecedorView.as_view(), name='deletar_fornecedor'),
    # path('atendimento/<uuid:pk>/', AtendimentoView.as_view(), name='atendimento'),
    # path('criar/<uuid:pk>/', AtendimentoRedirect.as_view(), name='criar_atendimento'),
]