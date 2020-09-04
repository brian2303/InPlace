from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from apps.inventario.models import CompraInsumos
from django.http import JsonResponse
from apps.inventario.forms import CompraInsumosForm

class CompraInsumosCreateView(CreateView):
    model = CompraInsumos
    form_class = CompraInsumosForm
    success_url = reverse_lazy('index')
    template_name = "compras/create.html"
    
    """recibe la solicitud de registro de compra con su detalle"""
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No se ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    """retorna este contexto cuando se pida la vista por get"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de compra'
        context['entity']  = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context