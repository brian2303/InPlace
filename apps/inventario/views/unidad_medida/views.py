from django.shortcuts import render
from django.urls import reverse_lazy
# clases genericas
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# modelos y formularios de unidades de medida
from apps.inventario.models import UnidadMedida
from apps.inventario.forms import UnidadMedidaForm

"""Listar unidad de medida"""
class UnidadMedidaListView(ListView):
    model = UnidadMedida
    template_name = "unidad_medida/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de unidades de medida'
        context["url_list"] = reverse_lazy('unidadmedida_lista')
        context['url_create'] = reverse_lazy('unidadmedida_crear')
        return context

"""crear una unidad de medida"""
class UnidadMedidaCreateView(CreateView):
    model = UnidadMedida
    template_name = "unidad_medida/create.html"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('unidadmedida_lista')
    

"""modificar una unidad de medida"""
class UnidadMedidaUpdateView(UpdateView):
    model = UnidadMedida
    template_name = "unidad_medida/create.html"
    form_class = UnidadMedidaForm   
    success_url = reverse_lazy('unidadmedida_lista')

"""eliminar una unidad de medida"""
class UnidadMedidaDeleteView(DeleteView):
    model = UnidadMedida
    template_name = "unidad_medida/delete.html"
    success_url = reverse_lazy('unidadmedida_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de unidades de medida'
        context["url_list"] = reverse_lazy('unidadmedida_lista')
        return context
    
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)