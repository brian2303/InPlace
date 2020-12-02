from tablib import Dataset
from apps.comercial.resources import ClienteResource
from django.shortcuts import render
def importar(request):  
    #template = loader.get_template('export/importar.html')  
    if request.method == 'POST':  
        cliente_resource = ClienteResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevos_clientes = request.FILES['csvfile'] 
        #import pdb;pdb.set_trace(); 
        #print(nuevos_clientes)  
        imported_data = dataset.load(nuevos_clientes.read())  
        #print(dataset)  
        #print(imported_data)
        result = cliente_resource.import_data(dataset, dry_run=True) # Test the data import  
        #print(result.has_errors())  
        if not result.has_errors():  
            cliente_resource.import_data(dataset, dry_run=False) # Actually import now  
    return render(request, 'carga_comercial/importar.html')