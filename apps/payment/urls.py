from django.urls import path
from .views import AdcionarPagamentoOrcamentoView, EditarPagamentoOrcamentoView, DeletarPagamentoOrcamentoView


app_name = 'payment'


urlpatterns = [
    path('<uuid:pk>/', EditarPagamentoOrcamentoView.as_view(), name='payment_orcamento_edit'),
    path('novo/<uuid:pk>/', AdcionarPagamentoOrcamentoView.as_view(), name='payment_orcamento'),
    path('delete/<uuid:pk>/', DeletarPagamentoOrcamentoView.as_view(), name='delete_payment_orcamento'),

]