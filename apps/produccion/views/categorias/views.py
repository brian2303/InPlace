from django.shortcuts import render
from django.urls import reverse_lazy
# clases genericas
from django.views.generic import ListView

# modelo de clientes
from apps.produccion.models import Productos, CategoriaProductos

"""Listar categorias"""
class CategoriaProductosListView(ListView):
    model = CategoriaProductos
    template_name = "categorias/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de categorias'
        context["url_list"] = reverse_lazy('clientes_lista')
        return context