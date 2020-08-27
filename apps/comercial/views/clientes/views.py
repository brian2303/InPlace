from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView

# propias
from apps.comercial.models import Cliente,TelefonoCliente
from apps.comercial.forms import ClienteForm,TelefonoClienteForm

"""Listar clientes"""
class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self,request,*args,**kwargs):
        data = []
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if body['action'] == 'listar_telefonos':
            telefonos_cliente = TelefonoCliente.objects.filter(cliente_id=body['id'])
            for telefono in telefonos_cliente:
                telefono = model_to_dict(telefono)
                data.append(telefono)
            return JsonResponse(data,safe=False)

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de clientes'
        context["url_list"] = reverse_lazy('clientes_lista')
        context['url_create'] = reverse_lazy('cliente_crear')
        return context


"""crear un cliente"""
class ClienteCreateView(CreateView):
    model = Cliente
    template_name = "clientes/create.html"
    form_class = ClienteForm
    second_form_class = TelefonoClienteForm
    success_url = reverse_lazy('clientes_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Cliente'
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post(self,request,*args,**kwgars):
        self.object = self.get_object
        form = self.form_class(request.POST)
        telefonos = []
        telefonos.append(request.POST['celular'])
        if request.POST['telefono_opcional'] not in '':
            telefonos.append(request.POST['telefono_opcional'])
        if form.is_valid():
            cliente = form.save()
            for telefono in telefonos:
                cliente.telefonos.create(numero_telefono=telefono)
            cliente.save()
            return redirect('clientes_lista')
        else:
            return redirect('cliente_crear')
        