from import_export import resources
from .models import CategoriaProductos

class CategoriaProductosResource(resources.ModelResource):
    
    class Meta:
        model = CategoriaProductos