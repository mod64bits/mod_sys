from django.urls import path, include
from .views import ListaDeTickets, IniciarAtendimentoView, AtendimentoView, AtendimentoRedirect, UploadFile

app_name = 'tickets'



urlpatterns = [
    path('', ListaDeTickets.as_view(), name='lista_tickets'),
    path('upload/<uuid:pk>/', UploadFile.as_view(), name="upload"),
    path('iniciar/atendimento/<uuid:pk>/', IniciarAtendimentoView.as_view(), name='iniciar_atendimento'),
    path('atendimento/<uuid:pk>/', AtendimentoView.as_view(), name='atendimento'),
    path('criar/<uuid:pk>/', AtendimentoRedirect.as_view(), name='criar_atendimento'),
]