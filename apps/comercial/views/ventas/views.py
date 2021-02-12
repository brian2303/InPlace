from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from apps.comercial.models import Ventas,DetalleVenta
from apps.produccion.models import Productos
from django.http import JsonResponse
from apps.comercial.forms import VentasForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
import json
from django.db import transaction,DatabaseError
from apps.usuarios.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

"""crear una venta con su detalle"""
class VentasCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):

    model = Ventas
    form_class = VentasForm
    success_url = reverse_lazy('venta_crear')
    template_name = "ventas/create.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    """recibe la solicitud de registro de venta con su detalle"""
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_productos':
                data = []
                productos = Productos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for producto in productos:
                    if producto.cantidad == 0:
                        continue

                    item = producto.toJSON()
                    item['value'] = producto.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    try:
                        dict_venta = json.loads(request.POST['ventas'])
                        venta = Ventas()
                        venta.estado = dict_venta['estado']
                        venta.cliente_id = dict_venta['cliente']
                        venta.fecha = dict_venta['fecha']
                        venta.subtotal = float(dict_venta['subtotal'])
                        venta.iva = float(dict_venta['iva'])
                        venta.total = float(dict_venta['total'])
                        venta.save()
                        for producto in dict_venta['productos']:
                            detalle = DetalleVenta()
                            detalle.producto_id = producto['id']
                            detalle.venta_id = venta.pk
                            detalle.precio_venta = producto['precioventa']
                            detalle.cantidad = producto['cantidad']
                            detalle.subtotal = producto['subtotal']
                            producto_actualizar = Productos.objects.filter(id=producto['id']).first()
                            cant_producto = producto_actualizar.cantidad
                            producto_actualizar.cantidad -= producto['cantidad']
                            detalle.save()
                            producto_actualizar.save() 
                    except DatabaseError as e:
                            data = {
                                "error":f"{producto_actualizar.nombre} solo tiene {cant_producto} unds disponibles",
                                "without_stock":True
                                }
                
            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    """retorna este contexto cuando se pida la vista por get"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Venta'
        context['entity']  = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context




class VentasUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):

    model = Ventas
    form_class = VentasForm
    success_url = reverse_lazy('venta_crear')
    template_name = "ventas/create.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    """recibe la solicitud de actualizacion de venta con su detalle"""
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_productos':
                data = []
                productos = Productos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for producto in productos:
                    item = producto.toJSON()
                    item['value'] = producto.nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    dict_venta = json.loads(request.POST['ventas'])
                    venta = Ventas.objects.get(pk=self.get_object().id)
                    venta.estado = dict_venta['estado']
                    venta.cliente_id = dict_venta['cliente']
                    venta.fecha = dict_venta['fecha']
                    venta.subtotal = float(dict_venta['subtotal'])
                    venta.iva = float(dict_venta['iva'])
                    venta.total = float(dict_venta['total'])
                    venta.save()
                    venta.detalleventa_set.all().delete()
                    for producto in dict_venta['productos']:
                        detalle = DetalleVenta()
                        detalle.producto_id = producto['id']
                        detalle.venta_id = venta.pk
                        detalle.precio_venta = producto['precioventa']
                        detalle.cantidad = producto['cantidad']
                        detalle.subtotal = producto['subtotal']
                        detalle.save()

            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_products_details(self):
        data = []
        try:
            detalle_venta = DetalleVenta.objects.filter(venta_id=self.get_object().id)
            for detalle in detalle_venta:
                item = detalle.producto.toJSON()
                item['cantidad'] = detalle.cantidad
                item['precioventa'] = float(detalle.precio_venta) 
                item['subtotal'] = float(detalle.cantidad * detalle.precio_venta)
                item['nombre'] = detalle.producto.nombre
                item['categoria'] = detalle.producto.categoria.toJSON()
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
        context['detalle'] = self.get_products_details() 
        context['action'] = 'edit'
        return context


class VentasListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Ventas
    template_name = "ventas/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwgars):
        try:
            action = request.POST['action']
            if action == 'searchdatasale':
                data = []
                for venta in Ventas.objects.filter(estado='venta'):
                    data.append(venta.toJSON())
        except Exception as e:
            pass
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de ventas'
        context['url_create'] = reverse_lazy('venta_crear')
        return context
    

class CotizacionesListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Ventas
    template_name = "cotizaciones/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwgars):
        try:
            action = request.POST['action']
            if action == 'searchdatacotizaciones':
                data = []
                for venta in Ventas.objects.filter(estado='cotizacion'):
                    data.append(venta.toJSON())
        except Exception as e:
            pass
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cotizacion'
        context['url_create'] = reverse_lazy('venta_crear')
        return context


class VentasDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    
    model = Ventas
    template_name = 'ventas/delete.html'
    success_url = reverse_lazy('ventas_lista')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        estado = self.object.estado
        data['estado'] = estado
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['url_list'] = self.success_url
        return context


