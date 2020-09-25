from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# modelo de clientes
from apps.inventario.models import Insumos
from apps.inventario.forms import InsumosForm
from django.contrib.auth.mixins import LoginRequiredMixin
"""Listar insumos"""
class InsumosListView(LoginRequiredMixin,ListView):
    model = Insumos
    template_name = "insumos/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Supplies List'
        context["url_list"] = reverse_lazy('insumo_lista')
        context['url_create'] = reverse_lazy('insumo_crear')
        return context

"""crear un insumo"""
class InsumosCreateView(LoginRequiredMixin,CreateView):
    model = Insumos
    template_name = "insumos/create.html"
    form_class = InsumosForm
    success_url = reverse_lazy('insumo_lista')
    

"""modificar un insumo"""
class InsumosUpdateView(LoginRequiredMixin,UpdateView):
    model = Insumos
    template_name = "insumos/create.html"
    form_class = InsumosForm   
    success_url = reverse_lazy('insumo_lista')

"""eliminar un insumo"""
class InsumosDeleteView(LoginRequiredMixin,DeleteView):
    model = Insumos
    template_name = "insumos/delete.html"
    success_url = reverse_lazy('insumo_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Supplies List'
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