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
from apps.produccion.forms import ProductosForm

"""Listar Productos"""
class ProductosListView(LoginRequiredMixin,ListView):
    model = Productos
    template_name = "productos/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Products List'
        context["url_list"] = reverse_lazy('productos_lista')
        context['url_create'] = reverse_lazy('producto_crear')
        return context

"""crear un producto"""
class ProductosCreateView(LoginRequiredMixin,CreateView):
    model = Productos
    template_name = "productos/create.html"
    form_class = ProductosForm
    success_url = reverse_lazy('productos_lista')

"""modificar un producto"""
class ProductosUpdateView(LoginRequiredMixin,UpdateView):
    model = Productos
    template_name = "productos/create.html"
    form_class = ProductosForm    
    success_url = reverse_lazy('productos_lista')

"""eliminar un producto"""
class ProductosDeleteView(LoginRequiredMixin,DeleteView):
    model = Productos
    template_name = "productos/delete.html"
    success_url = reverse_lazy('productos_lista')

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