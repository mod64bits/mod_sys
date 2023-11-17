from django.urls import path
from .views import ListaDeTickets

app_name = 'tickets'


urlpatterns = [
    path('', ListaDeTickets.as_view(), name='lista_tickets'),
]