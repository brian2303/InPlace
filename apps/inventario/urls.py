from django.urls import path
from .views.proveedores.views import *

urlpatterns = [
    path('proveedor/lista',ProveedorListView.as_view(),name='proveedor_lista'),
    path('proveedor/crear',ProveedorCreateView.as_view(),name='proveedor_crear'),
    path('proveedor/editar/<int:pk>',ProveedorUpdateView.as_view(),name='proveedor_editar'),
    path('proveedor/eliminar/<int:pk>',ProveedorDeleteView.as_view(),name='proveedor_eliminar')
]