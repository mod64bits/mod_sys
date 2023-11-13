from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.dashboard import urls as dashboard_urls
from apps.clientes import urls as clientes_urls

urlpatterns = [
    path('', include(dashboard_urls)),
    path('clientes/', include(clientes_urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
