from apps.produccion.models import Productos, CategoriaProductos, Transportadora, TelefonoTransportadora
from django.forms import *

class CategoriaProductosForm(ModelForm):
    
    class Meta:
        model = CategoriaProductos
        fields = [
            'nombre_categoria',
        ]
        labels = {
            'nombre_categoria':'Category Name',
        }
        widgets = {
            'nombre_categoria':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Category Name...'
                }
            ),
        }

class ProductosForm(ModelForm):
    
    class Meta:
        model = Productos
        fields = [
            'nombre',
            'cantidad',
            'precio_unitario',
            'categoria',
        ]
        labels = {
            'nombre':'Name',
            'cantidad':'Quantity',
            'precio_unitario':'Unit Price',
            'categoria':'Category',
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Name...'
                }
            ),
            'cantidad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Quantity...'
                }
            ),
            'precio_unitario': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Unit Price...'
                }
            ),
            'categoria': Select(
                attrs={
                    'class':'form-control',
                    'placeholder':'Category...'
                }
            ),            
        }

class TransportadoraForm(ModelForm):
    
    class Meta:
        model = Transportadora
        fields = [
            'nombre',
            'ciudad',
            'direccion',
            'email',
        ]
        labels = {
            'nombre': 'Name',
            'ciudad':'City',
            'direccion':'Address',
            'email':'Email',
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Name...'
                }
            ),
            'ciudad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'City...'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Address...'
                }
            ),
            'email': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Email...'
                }
            )
        }



class TelefonoTransportadoraForm(ModelForm):
    
    class Meta:
        model = TelefonoTransportadora
        fields = '__all__'
        labels = {
            'numero_telefono':'Numero'
        }
        widgets = {
            'numero_telefono' : TextInput(attrs={'class':'form-control'})
        }
