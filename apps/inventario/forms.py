from apps.inventario.models import Proveedor,TelefonoProveedor
from django.forms import *

class ProveedorForm(ModelForm):
    
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'ciudad',
            'direccion',
        ]
        labels = {
            'nombre': 'Nombres',
            'ciudad':'Ciudad',
            'direccion':'Direccion',
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombres...'
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ciudad...'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Dirección...'
                }
            )
        }

class TelefonoProveedorForm(ModelForm):
    
    class Meta:
        model = TelefonoProveedor
        fields = '__all__'
        labels = {
            'numero_telefono':'Numero'
        }
        widgets = {
            'numero_telefono' : TextInput(attrs={'class':'form-control'})
        }