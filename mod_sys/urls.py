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
from apps.relatorios import urls as relatorios_urls
from apps.ordemdeservicos import urls as ordens_url
from apps.payment import urls as payment_urls
from apps.prints import urls as prints_urls

urlpatterns = [

    path('', include(dashboard_urls)),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('print/', include(prints_urls)),
    path('relatorios/', include(relatorios_urls)),
    path('pagamentos/', include(payment_urls)),
    path('orcamentos/', include(orcamentos_url)),
    path('ordens/', include(ordens_url)),
    path('produtos/', include(produtos_url)),
    path('servicos/', include(servicos_url)),
    path('tickets/', include(tickets_url)),
    path('clientes/', include(clientes_urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
