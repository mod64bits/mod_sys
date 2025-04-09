from django.urls import include, path
from rest_framework import routers
from .clientes.viewset import ClienteViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('', include(router.urls)),

]