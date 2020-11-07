from apps.comercial.models import Cliente,TelefonoCliente,Ventas
from django.forms import *

"""formularios para el crud de proveedores junto con telefonos"""
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
            'numero_identificacion':'Id',
            'nombres': 'Name',
            'apellidos':'Last Name',
            'direccion':'Address',
            'ciudad':'City',
            'email':'Email',
        }
        widgets = {
            'numero_identificacion':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Id...'
                }
            ),
            'nombres': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Name...'
                }
            ),
            'apellidos': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Last Name...'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Address...'
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'City...'
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


"""formulario para el registro de una venta"""
class VentasForm(ModelForm):

    class Meta:
        model = Ventas
        fields = '__all__'
        widgets = {
            'cliente':Select(
                attrs ={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                }
            ),
            'fecha' : DateInput(
                format = '%Y-%m-%d',
                attrs ={
                    'autocomplete':'off',
                    'class':'form-control datetimepicker-input',
                    'id':'fecha',
                    'data-target': '#fecha',
                    'data-toggle':'datetimepicker',
                }
            ),
            'iva' : TextInput(
                attrs = {
                    'disabled':True,
                    'class':'form-control',
                }
            ),
            'subtotal' : TextInput(
                attrs = {
                    'disabled':True,
                    'class':'form-control'
                }
            ),
            'total' : TextInput(
                attrs = {
                    'disabled':True,
                    'class':'form-control'
                }
            ),
            'estado' : Select(
                attrs = {
                    'class':'form-control'
                }
            )
        }