from django.urls import path
from . import views
from apps.produccion.views.categorias.views import CategoriaProductosListView

urlpatterns = [
    path('categoria/listar', CategoriaProductosListView.as_view()),
]