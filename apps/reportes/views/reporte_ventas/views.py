import os

from django.views.generic import TemplateView,View
from apps.reportes.forms import ReporteVentaForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from apps.comercial.models import Ventas,DetalleVenta,Cliente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class ReporteVentaView(LoginRequiredMixin,TemplateView):
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
    
class ReportView(View):
    def get(self, request, *args, **kwargs):
        template = get_template('ventas/general.html')
        ventas = Ventas.objects.all()
        usuario = request.user.username
        # import pdb; pdb.set_trace()
        context = {'title':'Reporte de ventas','ventas':ventas,'usuario':usuario}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')
        return response