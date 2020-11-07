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
from apps.produccion.models import Transportadora, TelefonoTransportadora
from apps.produccion.forms import TransportadoraForm, TelefonoTransportadoraForm

"""Listar Transportadoras"""
class TransportadoraListView(LoginRequiredMixin,ListView):
    model = Transportadora
    template_name = "transportadora/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self,request,*args,**kwargs):
        data = []
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if body['action'] == 'listar_telefonos':
            telefonos_transportadora = TelefonoTransportadora.objects.filter(transportadora_id=body['id'])
            for telefono in telefonos_transportadora:
                telefono = model_to_dict(telefono)
                data.append(telefono)
            return JsonResponse(data,safe=False)

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Carriers List'
        context["url_list"] = reverse_lazy('transportadoras_lista')
        context['url_create'] = reverse_lazy('transportadora_crear')
        return context


"""Crear una Transportadora"""
class TransportadoraCreateView(LoginRequiredMixin,CreateView):
    model = Transportadora
    template_name = "transportadora/create.html"
    form_class = TransportadoraForm
    second_form_class = TelefonoTransportadoraForm
    success_url = reverse_lazy('transportadoras_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar Transportadora'
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
            transportadora = form.save()
            for telefono in telefonos:
                transportadora.telefonos.create(numero_telefono=telefono)
            transportadora.save()
            return redirect('transportadoras_lista')
        else:
            return redirect('transportadora_crear')
        

"""Modificar Transportadora"""
class TransportadoraUpdateView(LoginRequiredMixin,UpdateView):
    model = Transportadora
    template_name = "transportadora/create.html"
    form_class = TransportadoraForm
    second_form_class = TelefonoTransportadoraForm
    success_url = reverse_lazy('transportadoras_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Transportadora'
        context['id_transportadora'] = context['object'].pk
        telefonos_transportadora = context['object'].telefonos.all()
        context['celular'] = telefonos_transportadora[0].numero_telefono
        if len(telefonos_transportadora) == 2:
            context['telefono_opcional'] = telefonos_transportadora[1].numero_telefono
        return context
    
    def post(self,request,*args,**kwgars):
        # se esta creando una instancia del objeto que recibimos como llave primaria
        self.object = self.get_object
        transportadora = Transportadora.objects.get(pk=request.POST['transportadora_id'])
        form = self.form_class(request.POST,instance=transportadora)
        if form.is_valid():
            transportadora = form.save(commit=False)
            celular = transportadora.telefonos.first()
            celular.numero_telefono = request.POST['celular']
            celular.save()
            if len(transportadora.telefonos.all()) == 2:
                telefono_opcional = transportadora.telefonos.last()
                telefono_opcional.numero_telefono = request.POST['telefono_opcional']
                telefono_opcional.save()
            elif 'telefono_opcional' in request.POST and request.POST['telefono_opcional'] != '':
                transportadora.telefonos.create(numero_telefono=request.POST['telefono_opcional'])
            transportadora.save()
            return redirect('transportadoras_lista')
        else:
            return redirect('transportadora_crear')




"""Eliminar una Transportadora"""
class TransportadoraDeleteView(LoginRequiredMixin,DeleteView):
    model = Transportadora
    template_name = "transportadora/delete.html"
    success_url = reverse_lazy('transportadoras_lista')

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