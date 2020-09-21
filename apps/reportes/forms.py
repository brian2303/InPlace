from django.forms import *
from apps.comercial.models import Cliente
from apps.inventario.models import Proveedor
class ReporteVentaForm(Form):
    
    rango_fecha = CharField(widget=TextInput(
        attrs = {
            'class':'form-control',
            'autocomplete':'off'
        }
    ))
    cliente = ModelChoiceField(
        queryset=Cliente.objects.all()
    )


class ReporteCompraForm(forms.Form):
    rango_fecha = CharField(widget=TextInput(
        attrs = {
            'class':'form-control',
            'autocomplete':'off'
        }
    ))
    proveedor = ModelChoiceField(
        queryset=Proveedor.objects.all()
    )
