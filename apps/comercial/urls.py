from django.urls import path

# rutas de las vistas del crud de clientes.
from apps.comercial.views.clientes.views import *

urlpatterns = [
    path('clientes/lista',ClienteListView.as_view(),name='clientes_lista'),
    # path('clientes/lista/<int:pk>/',
    #     TelefonoClienteListView.as_view()
    #     ,name='telefonoscliente'
    # )
]