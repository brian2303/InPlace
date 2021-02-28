from django.contrib import admin
from django.urls import path,include
from apps.landing_page.views import IndexView,IndexViewEnglish
from apps.login.views import DashboardView
# Administración de Imagenes en Django
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('correos/',include('apps.correos.urls')),
    path('admin/', admin.site.urls),
    # reportes
    path('reportes/',include('apps.reportes.urls')),
    # index dos idiomas
    path('', IndexView.as_view(),name='index'),
    path('en/', IndexViewEnglish.as_view(),name='index_english'),
    #url para graficos
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    # Modulos
    path('comercial/',include('apps.comercial.urls')),
    path('inventario/',include('apps.inventario.urls')),
    path('produccion/',include('apps.produccion.urls')),
    path('usuarios/',include('apps.usuarios.urls')),
    # Login
    path('login/',include('apps.login.urls'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
