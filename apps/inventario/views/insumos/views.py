from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
# Logon y Privilegios en el Sistema
from apps.usuarios.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# modelo de clientes
from apps.inventario.models import Insumos
from apps.inventario.forms import InsumosForm

"""Listar insumos"""
class InsumosListView(LoginRequiredMixin,ListView):
    model = Insumos
    template_name = "insumos/list.html"
    permission_required = 'view_insumos'

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Insumos'
        context["url_list"] = reverse_lazy('insumo_lista')
        context['url_create'] = reverse_lazy('insumo_crear')
        return context

"""crear un insumo"""
class InsumosCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Insumos
    template_name = "insumos/create.html"
    form_class = InsumosForm
    success_url = reverse_lazy('insumo_lista')
    permission_required = 'add_insumos'
    
"""modificar un insumo"""
class InsumosUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Insumos
    template_name = "insumos/create.html"
    form_class = InsumosForm   
    success_url = reverse_lazy('insumo_lista')
    permission_required = 'update_insumos'

"""eliminar un insumo"""
class InsumosDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Insumos
    template_name = "insumos/delete.html"
    success_url = reverse_lazy('insumo_lista')
    permission_required = 'delete_insumos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Insumos'
        context["url_list"] = reverse_lazy('insumo_lista')
        return context
    
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)