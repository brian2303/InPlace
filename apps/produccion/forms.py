from apps.produccion.models import Productos, CategoriaProductos, Transportadora, TelefonoTransportadora
from django.forms import *

class CategoriaProductosForm(ModelForm):
    
    class Meta:
        model = CategoriaProductos
        fields = [
            'nombre_categoria',
        ]
        labels = {
            'nombre_categoria':'Nombre Categoría',
        }
        widgets = {
            'nombre_categoria':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre Categoría...'
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
            'nombre':'Nombre',
            'cantidad':'Cantidad',
            'precio_unitario':'Precio Unitario',
            'categoria':'Categoría',
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre...'
                }
            ),
            'cantidad': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Cantidad...'
                }
            ),
            'precio_unitario': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Precio Unitario...'
                }
            ),
            'categoria': Select(
                attrs={
                    'class':'form-control',
                    'placeholder':'Categoría...'
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
            'nombre': 'Nombre',
            'ciudad':'Ciudad',
            'direccion':'Direccion',
            'email':'Email',
        }
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre...'
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
