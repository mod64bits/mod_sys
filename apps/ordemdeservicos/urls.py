from django.urls import path

from .views import OrdensLista, NovaOrdem


app_name = 'ordens'

urlpatterns = [
    path('', OrdensLista.as_view(), name='lista_ordens'),
    path('nova/', NovaOrdem.as_view(), name='nova_ordem'),

]
