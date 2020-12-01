from import_export import resources
from .models import Cliente

class ClienteResource(resources.ModelResource):
    
    class Meta:
        model = Cliente