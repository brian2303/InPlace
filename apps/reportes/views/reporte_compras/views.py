from django.views.generic import TemplateView
from apps.reportes.forms import ReporteCompraForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from apps.inventario.models import CompraInsumos,Proveedor

class ReporteCompraView(TemplateView):
    template_name = "compras/reporte.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'buscar_reporte_fecha':
                data = []
                fecha_inicial = request.POST['fecha_inicial']
                fecha_final = request.POST['fecha_final']
                if len(fecha_inicial) and len(fecha_final):
                    compras = CompraInsumos.objects.filter(
                        fecha__range=[fecha_inicial,fecha_final]
                    )
                for compra in compras:
                    data.append(compra.toJSON())
            elif action == 'buscar_reporte_proveedor':
                data = []
                compras = CompraInsumos.objects.filter(proveedor_id=request.POST['proveedor'])
                for compra in compras:
                    data.append(compra.toJSON())
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Reporte de Compras'
        context["form"] = ReporteCompraForm()
        return context