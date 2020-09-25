from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.comercial.models import Ventas
from datetime import datetime
from django.db.models.functions import Coalesce
from django.db.models import Sum
# Create your views here.

class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesion' 
        return context

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "base/dashboard.html"
    
    def get_sales_data(self):
        data = []
        year = datetime.now().year
        for m in range(1,13):
            total = Ventas.objects.filter(fecha__year=year,fecha__month=m).aggregate(
                r=Coalesce(Sum('total'),0)).get('r')
            data.append(float(total))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Dashboard'
        context['ventas_mes_a_mes'] = self.get_sales_data() 
        return context
    
