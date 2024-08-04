from django.urls import path
from .views import AdcionarPagamentoOrcamentoView, EditarPagamentoOrcamentoView


app_name = 'payment'


urlpatterns = [
    path('<uuid:pk>/', EditarPagamentoOrcamentoView.as_view(), name='payment_orcamento_edit'),
    path('novo/<uuid:pk>/', AdcionarPagamentoOrcamentoView.as_view(), name='payment_orcamento'),

]