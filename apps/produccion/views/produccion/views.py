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
# modelo de Produccion
from apps.produccion.models import OrdenProduccion
from apps.produccion.forms import OrdenProduccionForm

"""Listar Ordenes de producción"""
class OrdenProduccionListView(LoginRequiredMixin,ListView):
    model = OrdenProduccion
    template_name = "produccion/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de ordenes'
        context["url_list"] = reverse_lazy('produccion_listar')
        context['url_create'] = reverse_lazy('produccion_crear')
        context['entity'] = 'Produccion'
        return context

"""crear una orden de produccion"""
class OrdenProduccionCreateView(LoginRequiredMixin,CreateView):
    model = OrdenProduccion
    template_name = "produccion/create.html"
    form_class = OrdenProduccionForm
    success_url = reverse_lazy('produccion_listar')

# """modificar un producto"""
# class ProductosUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
#     model = Productos
#     template_name = "productos/create.html"
#     form_class = ProductosForm    
#     success_url = reverse_lazy('productos_lista')

# """eliminar un producto"""
# class ProductosDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
#     model = Productos
#     template_name = "productos/delete.html"
#     success_url = reverse_lazy('productos_lista')

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
    
#     def post(self,request,*args,**kwgars):
#         data = {}
#         try:
#             self.object = self.get_object()
#             self.object.delete()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
        