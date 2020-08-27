from django.urls import path

# rutas de las vistas del crud de clientes.
from apps.comercial.views.clientes.views import *

urlpatterns = [
    path('clientes/lista',ClienteListView.as_view(),name='clientes_lista'),
    path('clientes/crear',ClienteCreateView.as_view(),name='cliente_crear')
]