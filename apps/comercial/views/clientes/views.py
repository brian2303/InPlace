from django.shortcuts import render
from django.urls import reverse_lazy
# clases genericas
from django.views.generic import ListView

# modelo de clientes
from apps.comercial.models import Cliente,TelefonoCliente

"""Listar clientes"""
class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/list.html"

    # CONTEXTO A ENVIAR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Listado de clientes'
        context["url_list"] = reverse_lazy('clientes_lista')
        return context


"""pedir telefonos por ajax"""
# class TelefonoClienteListView(ListView):
#     model = TelefonoCliente
#     template_name = "clientes/list.html"
#     def post(self,request,*args,**kwargs):
#         post = request.POST
#         print(post)
#         import pdb; pdb.set_trace()
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add':
#                 form = self.get_form()
#             else:
#                 data['error'] = 'No ha ingresado ninguna opcion'
#         except Exception as e :
#             data['error'] = str(e)
#         return JsonResponse(data)



