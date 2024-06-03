from django.urls import path

from .views import OrdensLista, NovaOrdem, OrdemDeServico


app_name = 'ordens'

urlpatterns = [
    path('', OrdensLista.as_view(), name='lista_ordens'),
    path('nova/', NovaOrdem.as_view(), name='nova_ordem'),
    path('editar/<uuid:pk>/', OrdemDeServico.as_view(), name='editar_ordem'),

]
