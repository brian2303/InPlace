from django.shortcuts import render
from django.urls import reverse_lazy
# clases genericas
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# modelo de transportadoras
from apps.produccion.models import Productos, CategoriaProductos
from apps.produccion.forms import CategoriaProductosForm

"""Listar categorias"""
class CategoriaProductosListView(LoginRequiredMixin,ListView):
    model = CategoriaProductos
    template_name = "categorias/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Categories List'
        context["url_list"] = reverse_lazy('categorias_lista')
        context['url_create'] = reverse_lazy('categoria_crear')
        return context

"""crear una categoría"""
class CategoriaProductosCreateView(LoginRequiredMixin,CreateView):
    model = CategoriaProductos
    template_name = "categorias/create.html"
    form_class = CategoriaProductosForm
    success_url = reverse_lazy('categorias_lista')
    
"""modificar una categoría"""
class CategoriaProductosUpdateView(LoginRequiredMixin,UpdateView):
    model = CategoriaProductos
    template_name = "categorias/create.html"
    form_class = CategoriaProductosForm    
    success_url = reverse_lazy('categorias_lista')

"""eliminar una categoría"""
class CategoriaProductosDeleteView(LoginRequiredMixin,DeleteView):
    model = CategoriaProductos
    template_name = "categorias/delete.html"
    success_url = reverse_lazy('categorias_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)