from django.urls import path
# permite mapear la ruta para ubicar la vista del crud (linea 5)
from . import views
# rutas de las vistas del crud de categoria.
from apps.produccion.views.categorias.views import *
from apps.produccion.views.productos.views import *
from apps.produccion.views.transportadora.views import *

urlpatterns = [
    path('categoria/lista', CategoriaProductosListView.as_view(),name='categorias_lista'),
    path('categoria/crear', CategoriaProductosCreateView.as_view(),name='categoria_crear'),
    path('categoria/editar/<int:pk>',CategoriaProductosUpdateView.as_view(),name='categoria_editar'),
    path('categoria/eliminar/<int:pk>',CategoriaProductosDeleteView.as_view(),name='categoria_eliminar'),
    path('productos/lista', ProductosListView.as_view(),name='productos_lista'),
    path('productos/crear', ProductosCreateView.as_view(),name='producto_crear'),
    path('productos/editar/<int:pk>',ProductosUpdateView.as_view(),name='producto_editar'),
    path('productos/eliminar/<int:pk>',ProductosDeleteView.as_view(),name='producto_eliminar'),
    path('transportadora/lista', TransportadoraListView.as_view(),name='transportadoras_lista'),
    path('transportadora/crear', TransportadoraCreateView.as_view(),name='transportadora_crear'),
    path('transportadora/editar/<int:pk>',TransportadoraUpdateView.as_view(),name='transportadora_editar'),
    path('transportadora/eliminar/<int:pk>',TransportadoraDeleteView.as_view(),name='transportadora_eliminar'),
]