from apps.inventario.models import *
from django.forms import *

# ==== Formularios para el crud de proveedores ====
"""formulario para registrar y editar el proveedor"""
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
"""formulario para mapear los telefonos del proveedor """
class TelefonoProveedorForm(ModelForm):
    
    class Meta:
        model = TelefonoProveedor
        fields = '__all__'
        labels = {
            'numero_telefono':'Numero'
        }
        widgets = {
            'numero_telefono' : TextInput(attrs={'class':'form-control','maxlength':15}),

        }


# ==== Formularios para el crud de insumos ====
"""formulario para registrar y editar un insumo"""
class InsumosForm(ModelForm):
    class Meta:
        model = Insumos 
        fields = '__all__'
        labels = {
            'nombre' : 'Nombre de insumo: ',
            'cantidad': 'Cantidad: ',
            'unidad_medida': 'Unidad de medida: ',
        }
        widgets = {
            'nombre' : TextInput(
                attrs={
                    'class':'form-control',
                    'autofocus':'autofocus'
                }
            ),
            'cantidad' : NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidad_medida': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione la unidad de medida...'
                }
            )
        }

"""formulario para registrar y editar una unidad de medida"""
class UnidadMedidaForm(ModelForm):
    
    class Meta:
        model = UnidadMedida
        fields = '__all__'
        labels = {
            'nombre':'Nombre unidad de medida:',
            'abreviatura':'Abreviatura: ',
        }
        widgets = {
            'nombre':TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'abreviatura': TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
        }

# === Formulario para crear una compra ===

class CompraInsumosForm(ModelForm):
    
    """definiendo unas clases para cada componente de mi formulario"""
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CompraInsumos
        fields = '__all__'
        widgets = {
            'proveedor':Select(
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
            )
        }
