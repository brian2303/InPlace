from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# propias
from apps.comercial.models import Cliente,TelefonoCliente
from apps.comercial.forms import ClienteForm,TelefonoClienteForm

"""Listar clientes"""
class ClienteListView(LoginRequiredMixin,ListView):
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
class ClienteCreateView(LoginRequiredMixin,CreateView):
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
        

"""modificar cliente"""
class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Cliente
    template_name = "clientes/create.html"
    form_class = ClienteForm
    second_form_class = TelefonoClienteForm
    success_url = reverse_lazy('clientes_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['id_cliente'] = context['object'].pk
        telefonos_cliente = context['object'].telefonos.all()
        context['celular'] = telefonos_cliente[0].numero_telefono
        if len(telefonos_cliente) == 2:
            context['telefono_opcional'] = telefonos_cliente[1].numero_telefono
        return context
    
    def post(self,request,*args,**kwgars):
        # se esta creando una instancia del objeto que recibimos como llave primaria
        self.object = self.get_object
        cliente = Cliente.objects.get(pk=request.POST['cliente_id'])
        form = self.form_class(request.POST,instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            celular = cliente.telefonos.first()
            celular.numero_telefono = request.POST['celular']
            celular.save()
            if len(cliente.telefonos.all()) == 2:
                telefono_opcional = cliente.telefonos.last()
                telefono_opcional.numero_telefono = request.POST['telefono_opcional']
                telefono_opcional.save()
            elif 'telefono_opcional' in request.POST and request.POST['telefono_opcional'] != '':
                cliente.telefonos.create(numero_telefono=request.POST['telefono_opcional'])
            cliente.save()
            return redirect('clientes_lista')
        else:
            return redirect('cliente_crear')




"""eliminar un cliente"""
class ClienteDeleteView(LoginRequiredMixin,DeleteView):
    model = Cliente
    template_name = "clientes/delete.html"
    success_url = reverse_lazy('clientes_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)