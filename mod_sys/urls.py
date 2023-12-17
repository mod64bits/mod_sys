from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.dashboard import urls as dashboard_urls
from apps.clientes import urls as clientes_urls
from apps.ticket import urls as tickets_url
from apps.produtos import urls as produtos_url
from apps.servicos import urls as servicos_url
from apps.orcamentos import urls as orcamentos_url

urlpatterns = [

    path('', include(dashboard_urls)),
    path('orcamentos/', include(orcamentos_url)),
    path('produtos/', include(produtos_url)),
    path('servicos/', include(servicos_url)),
    path('tickets/', include(tickets_url)),
    path('clientes/', include(clientes_urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
