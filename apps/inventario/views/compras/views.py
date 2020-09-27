from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from apps.inventario.models import *
from django.http import JsonResponse
from apps.inventario.forms import CompraInsumosForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
import json
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.usuarios.mixins import ValidatePermissionRequiredMixin

class CompraInsumosCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):

    model = CompraInsumos
    form_class = CompraInsumosForm
    success_url = reverse_lazy('compra_crear')
    template_name = "compras/create.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    """recibe la solicitud de registro de compra con su detalle"""
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_insumos':
                data = []
                insumos = Insumos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for insumo in insumos:
                    item = insumo.toJSON()
                    item['value'] = insumo.nombre
                    data.append(item)
            elif action == 'add': 
                with transaction.atomic():
                    dict_compra = json.loads(request.POST['compras'])
                    compra = CompraInsumos()
                    compra.proveedor_id = dict_compra['proveedor']
                    compra.fecha = dict_compra['fecha']
                    compra.subtotal = float(dict_compra['subtotal'])
                    compra.iva = float(dict_compra['iva'])
                    compra.total = float(dict_compra['total'])
                    compra.save()
                    for insumo in dict_compra['insumos']:
                        detalle = DetalleCompra()
                        detalle.insumo_id = insumo['id']
                        detalle.compra_id = compra.pk
                        detalle.precio_compra = insumo['preciocompra']
                        detalle.cantidad = insumo['cantidad']
                        detalle.subtotal = insumo['subtotal']
                        detalle.save()
            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    """retorna este contexto cuando se pida la vista por get"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de compra'
        context['entity']  = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class CompraInsumosUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):

    model = CompraInsumos
    form_class = CompraInsumosForm
    success_url = reverse_lazy('compra_crear')
    template_name = "compras/create.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    """recibe la solicitud de registro de compra con su detalle"""
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_insumos':
                data = []
                insumos = Insumos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for insumo in insumos:
                    item = insumo.toJSON()
                    item['value'] = insumo.nombre
                    data.append(item)
            elif action == 'edit': 
                with transaction.atomic():
                    dict_compra = json.loads(request.POST['compras'])
                    compra = CompraInsumos.objects.get(pk=self.get_object().id)
                    compra.proveedor_id = dict_compra['proveedor']
                    compra.fecha = dict_compra['fecha']
                    compra.subtotal = float(dict_compra['subtotal'])
                    compra.iva = float(dict_compra['iva'])
                    compra.total = float(dict_compra['total'])
                    compra.save()
                    compra.detallecompra_set.all().delete()
                    for insumo in dict_compra['insumos']:
                        detalle = DetalleCompra()
                        detalle.insumo_id = insumo['id']
                        detalle.compra_id = compra.pk
                        detalle.precio_compra = insumo['preciocompra']
                        detalle.cantidad = insumo['cantidad']
                        detalle.subtotal = insumo['subtotal']
                        detalle.save()
            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_insumos_details(self):
        data = []
        try:
            detalle_compras = DetalleCompra.objects.filter(compra_id=self.get_object().id)
            for detalle in detalle_compras:
                item = detalle.insumo.toJSON()
                item['cantidad'] = detalle.cantidad
                item['preciocompra'] = float(detalle.precio_compra) 
                item['subtotal'] = float(detalle.cantidad * detalle.precio_compra) 
                data.append(item)
        except:
            pass
        return data

    """retorna este contexto cuando se pida la vista por get"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de compra'
        context['entity']  = 'Compras'
        context['list_url'] = self.success_url
        context['detalle'] = self.get_insumos_details() 
        context['action'] = 'edit'
        return context


class CompraInsumosListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = CompraInsumos
    template_name = "compras/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwgars):
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for compra in CompraInsumos.objects.all():
                    data.append(compra.toJSON())
        except Exception as e:
            pass
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de compras'
        context['url_create'] = reverse_lazy('compra_crear')
        return context
    

class CompraInsumosDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = CompraInsumos
    template_name = 'compras/delete.html'
    success_url = reverse_lazy('compra_lista')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Compra'
        context['url_list'] = self.success_url
        return context