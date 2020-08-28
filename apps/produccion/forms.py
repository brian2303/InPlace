from apps.produccion.models import Productos, CategoriaProductos
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
            'categoria': TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Categoría...'
                }
            ),            
        }