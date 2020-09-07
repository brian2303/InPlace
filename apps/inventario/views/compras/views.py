from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from apps.inventario.models import *
from django.http import JsonResponse
from apps.inventario.forms import CompraInsumosForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
import json
class CompraInsumosCreateView(CreateView):
    model = CompraInsumos
    form_class = CompraInsumosForm
    success_url = reverse_lazy('index')
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
                data['success'] = 'Registro Exitoso'
            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    """retorna este contexto cuando se pida la vista por get"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register Purchase'
        context['entity']  = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context