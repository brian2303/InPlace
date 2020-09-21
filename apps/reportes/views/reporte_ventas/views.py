from django.views.generic import TemplateView
from apps.reportes.forms import ReporteVentaForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from apps.comercial.models import Ventas,DetalleVenta,Cliente

class ReporteVentaView(TemplateView):
    template_name = "ventas/reporte.html"

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
                    ventas = Ventas.objects.filter(
                        fecha__range=[fecha_inicial,fecha_final]
                    )
                for venta in ventas:
                    data.append(venta.toJSON())
            elif action == 'buscar_reporte_cliente':
                data = []
                ventas = Ventas.objects.filter(cliente_id=request.POST['cliente'])
                for venta in ventas:
                    data.append(venta.toJSON())
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Reporte de ventas'
        context["form"] = ReporteVentaForm()
        return context
    
