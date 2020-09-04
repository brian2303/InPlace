from django.urls import path
from .views.proveedores.views import *
from .views.unidad_medida.views import *
from .views.insumos.views import *
from .views.compras.views import *

urlpatterns = [
    # proveedor
    path('proveedor/lista',ProveedorListView.as_view(),name='proveedor_lista'),
    path('proveedor/crear',ProveedorCreateView.as_view(),name='proveedor_crear'),
    path('proveedor/editar/<int:pk>',ProveedorUpdateView.as_view(),name='proveedor_editar'),
    path('proveedor/eliminar/<int:pk>',ProveedorDeleteView.as_view(),name='proveedor_eliminar'),
    # unidad de medida
    path('unidadmedida/lista',UnidadMedidaListView.as_view(),name='unidadmedida_lista'),
    path('unidadmedida/crear',UnidadMedidaCreateView.as_view(),name='unidadmedida_crear'),
    path('unidadmedida/editar/<int:pk>',UnidadMedidaUpdateView.as_view(),name='unidadmedida_editar'),
    path('unidadmedida/eliminar/<int:pk>',UnidadMedidaDeleteView.as_view(),name='unidadmedida_eliminar'),
    # insumo
    path('insumo/lista',InsumosListView.as_view(),name='insumo_lista'),
    path('insumo/crear',InsumosCreateView.as_view(),name='insumo_crear'),
    path('insumo/editar/<int:pk>',InsumosUpdateView.as_view(),name='insumo_editar'),
    path('insumo/eliminar/<int:pk>',InsumosDeleteView.as_view(),name='insumo_eliminar'),
    
    #compra
    path('compra/crear',CompraInsumosCreateView.as_view(),name='compra_crear'),

]