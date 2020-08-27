from apps.comercial.models import Cliente,TelefonoCliente
from django.forms import *

class ClienteForm(ModelForm):
    
    class Meta:
        model = Cliente
        fields = [
            'numero_identificacion',
            'nombres',
            'apellidos',
            'direccion',
            'ciudad',
            'email',
        ]
        labels = {
            'numero_identificacion':'Numero identificacion',
            'nombres': 'Nombres',
            'apellidos':'Apellidos',
            'direccion':'Direccion',
            'ciudad':'Ciudad',
            'email':'Email',
        }
        widgets = {
            'numero_identificacion':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nro de identificación...'
                }
            ),
            'nombres': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombres...'
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'apellidos...'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Dirección...'
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ciudad...'
                }
            ),
            'email': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Email...'
                }
            )
        }



class TelefonoClienteForm(ModelForm):
    
    class Meta:
        model = TelefonoCliente
        fields = '__all__'
        labels = {
            'numero_telefono':'Numero'
        }
        widgets = {
            'numero_telefono' : TextInput(attrs={'class':'form-control'})
        }

