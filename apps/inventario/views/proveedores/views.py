# importanciones propias de django
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# importaciones propias del proyecto
from apps.inventario.models import Proveedor,TelefonoProveedor
from apps.inventario.forms import ProveedorForm,TelefonoProveedorForm


"""Listar proveedores"""
class ProveedorListView(ListView):
    model = Proveedor
    template_name = "proveedor/list.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self,request,*args,**kwargs):
        data = []
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if body['action'] == 'listar_telefonos':
            telefonos_proveedor = TelefonoProveedor.objects.filter(proveedor_id=body['id'])
            for telefono in telefonos_proveedor:
                telefono = model_to_dict(telefono)
                data.append(telefono)
            return JsonResponse(data,safe=False)

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de proveedores'
        context["url_list"] = reverse_lazy('proveedor_lista')
        context['url_create'] = reverse_lazy('proveedor_crear')
        return context


"""crear proveedor"""
class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = "proveedor/create.html"
    form_class = ProveedorForm
    second_form_class = TelefonoProveedorForm
    success_url = reverse_lazy('proveedor_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar proveedor'
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
            proveedor = form.save()
            for telefono in telefonos:
                proveedor.telefonos.create(numero_telefono=telefono)
            proveedor.save()
            return redirect('proveedor_lista')
        else:
            return redirect('proveedor_crear')


"""modificar proveedor"""
class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = "proveedor/create.html"
    form_class = ProveedorForm
    second_form_class = TelefonoProveedorForm
    success_url = reverse_lazy('proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Proveedor'
        context['id_proveedor'] = context['object'].pk
        telefonos_proveedor = context['object'].telefonos.all()
        context['celular'] = telefonos_proveedor[0].numero_telefono
        if len(telefonos_proveedor) == 2:
            context['telefono_opcional'] = telefonos_proveedor[1].numero_telefono
        return context
    
    def post(self,request,*args,**kwgars):
        # se esta creando una instancia del objeto que recibimos como llave primaria
        self.object = self.get_object
        proveedor = Proveedor.objects.get(pk=request.POST['proveedor_id'])
        form = self.form_class(request.POST,instance=proveedor)
        if form.is_valid():
            proveedor = form.save(commit=False)
            celular = proveedor.telefonos.first()
            celular.numero_telefono = request.POST['celular']
            celular.save()
            if len(proveedor.telefonos.all()) == 2:
                telefono_opcional = proveedor.telefonos.last()
                telefono_opcional.numero_telefono = request.POST['telefono_opcional']
                telefono_opcional.save()
            elif 'telefono_opcional' in request.POST and request.POST['telefono_opcional'] != '':
                proveedor.telefonos.create(numero_telefono=request.POST['telefono_opcional'])
            proveedor.save()
            return redirect('proveedor_lista')
        else:
            return redirect('proveedor_crear')

"""eliminar un proveedor"""
class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = "proveedor/delete.html"
    success_url = reverse_lazy('proveedor_lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de proveedores'
        context["url_list"] = reverse_lazy('proveedor_lista')
        return context
    
    def post(self,request,*args,**kwgars):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)