from django.urls import path
# permite mapear la ruta para ubicar la vista del crud (linea 5)
from . import views
# rutas de las vistas del crud de categoria.
from apps.produccion.views.categorias.views import *

urlpatterns = [
    path('categoria/lista', CategoriaProductosListView.as_view(),name='categoria_lista'),
]