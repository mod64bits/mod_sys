from django.urls import path

from .views import OrdensLista, NovaOrdem, OrdemDeServicoDetalhe, export_ordem_pdf, MudarStatusOrdem


app_name = 'ordens'

urlpatterns = [
    path('', OrdensLista.as_view(), name='lista_ordens'),
    path('nova/', NovaOrdem.as_view(), name='nova_ordem'),
    path('editar/<uuid:pk>/', OrdemDeServicoDetalhe.as_view(), name='editar_ordem'),
    path('mudar/status/<uuid:pk>/', MudarStatusOrdem.as_view(), name='mudar_os_status'),
    path('export-pdf/<uuid:id>/', export_ordem_pdf, name='export-pdf'),

]
