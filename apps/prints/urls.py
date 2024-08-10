from django.urls import path
from .views import PrintView

app_name = 'prints'


urlpatterns = [
    path('orcamento/<uuid:pk>/', PrintView.as_view(), name='print_orcamento'),

]