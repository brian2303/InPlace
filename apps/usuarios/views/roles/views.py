from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
# clases genericas
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
# modelo de Usuarios
from apps.usuarios.models import User
from apps.usuarios.forms import UserForm

from apps.usuarios.mixins import ValidatePermissionRequiredMixin


"""Listar Roles"""
class RolListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Group
    template_name = "roles/list.html"
    
    
    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de Roles'
        return context
