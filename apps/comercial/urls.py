from django.urls import path

# rutas de las vistas del crud de clientes.
from apps.comercial.views.clientes.views import *
from .views.ventas.views import VentasCreateView,VentasListView,CotizacionesListView,VentasDeleteView,VentasUpdateView
from apps.comercial.views.carga_comercial.views import importar

urlpatterns = [
    #Clientes y telefonos cliente
    path('clientes/lista',ClienteListView.as_view(),name='clientes_lista'),
    path('clientes/crear',ClienteCreateView.as_view(),name='cliente_crear'),
    path('clientes/editar/<int:pk>',ClienteUpdateView.as_view(),name='cliente_editar'),
    path('clientes/eliminar/<int:pk>',ClienteDeleteView.as_view(),name='cliente_eliminar'),
    # Ventas
    path('ventas/crear',VentasCreateView.as_view(),name='venta_crear'),
    path('ventas/lista',VentasListView.as_view(),name='ventas_lista'),
    path('cotizaciones/lista',CotizacionesListView.as_view(),name='cotizaciones_lista'),
    path('ventas/eliminar/<int:pk>',VentasDeleteView.as_view(),name='venta_eliminar'),
    path('ventas/editar/<int:pk>',VentasUpdateView.as_view(),name='venta_editar'),
    path('clientes/carga',importar,name="cliente_cargar"),
]