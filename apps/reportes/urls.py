from django.urls import path
from .views.reporte_ventas.views import ReporteVentaView,ReportView
from .views.reporte_compras.views import ReporteCompraView
urlpatterns = [
    path('general/',ReportView.as_view(),name='reporte'),
    path('ventas/',ReporteVentaView.as_view(),name='reporte_ventas'),
    path('compras/',ReporteCompraView.as_view(),name='reporte_compras'),
]