from rest_framework import viewsets

from .serializers import ClienteSerializer
from apps.clientes.models import Cliente


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()