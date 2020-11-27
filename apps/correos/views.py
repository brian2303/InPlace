from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives 
from django.conf import settings
from apps.comercial.models import Cliente


def send_email():    
    template = get_template('envio_correo.html')
    content = template.render()
    usuario = settings.EMAIL_HOST_USER 

    clientes = Cliente.objects.all()
    lista_clientes = []
    for cliente in clientes:
        lista_clientes.append(cliente.email)

    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'prueba inplace',
        settings.EMAIL_HOST_USER,
        lista_clientes,
    )

    email.attach_alternative(content,'text/html')
    email.send()
    #import pdb;pdb.set_trace();

def request_email(request):
    send_email()
    return redirect('clientes_lista')
