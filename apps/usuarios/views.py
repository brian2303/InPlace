from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
# clases genericas
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# modelo de transportadoras
from apps.usuarios.models import User
from apps.usuarios.forms import UserForm

from apps.usuarios.mixins import ValidatePermissionRequiredMixin
# from apps.usuarios.forms import UserForm
# from apps.usuarios.models import User

# Create your views here.

# def index_usuarios(request):
#     return render(request,'list.html')

"""Listar Usuarios"""
class UserListView(LoginRequiredMixin,ListView):
    model = User
    template_name = "list.html"
    
    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Usuarios'
        context["url_list"] = reverse_lazy('usuarios_lista')
        context['url_create'] = reverse_lazy('usuario_crear')
        return context

"""crear un usuario"""
class UserCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = User
    template_name = "create.html"
    form_class = UserForm
    success_url = reverse_lazy('usuarios_lista')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']            
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponseRedirect(reverse_lazy('usuarios_lista'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

        
"""modificar un usuario"""
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    template_name = "create.html"
    form_class = UserForm    
    success_url = reverse_lazy('usuarios_lista')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponseRedirect(reverse_lazy('usuarios_lista'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

"""eliminar un usuario"""
class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = "delete.html"
    success_url = reverse_lazy('usuarios_lista')

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