from django.shortcuts import render
from django.urls import reverse_lazy
# clases genericas
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from apps.usuarios.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# modelo de Productos
from apps.produccion.models import Productos, CategoriaProductos
from apps.produccion.forms import ProductosForm

"""Listar Productos"""
class ProductosListView(LoginRequiredMixin,ListView):
    model = Productos
    template_name = "productos/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Product.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de productos'
        context["url_list"] = reverse_lazy('productos_lista')
        context['url_create'] = reverse_lazy('producto_crear')
        context['entity'] = 'Productos'
        return context

"""crear un producto"""
class ProductosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Productos
    template_name = "productos/create.html"
    form_class = ProductosForm
    success_url = reverse_lazy('productos_lista')

"""modificar un producto"""
class ProductosUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Productos
    template_name = "productos/create.html"
    form_class = ProductosForm    
    success_url = reverse_lazy('productos_lista')

"""eliminar un producto"""
class ProductosDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
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
        