from django.urls import path
from .views import ListaDeTickets, IniciarAtendimentoView

app_name = 'tickets'


urlpatterns = [
    path('', ListaDeTickets.as_view(), name='lista_tickets'),
    path('atendimento/<uuid:pk>/', IniciarAtendimentoView.as_view(), name='iniciar_atendimento'),
]