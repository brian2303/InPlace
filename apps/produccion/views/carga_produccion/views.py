from tablib import Dataset
from apps.produccion.resources import CategoriaProductosResource
from django.shortcuts import render
def importar(request):  
    #template = loader.get_template('export/importar.html')  
    if request.method == 'POST':  
        categoria_resource = CategoriaProductosResource()  
        dataset = Dataset()  
        print(dataset)  
        nuevas_categorias = request.FILES['xlsxfile']  
        print(nuevas_categorias)  
        imported_data = dataset.load(nuevas_categorias.read())  
        print(dataset)  
        result = categoria_resource.import_data(dataset, dry_run=True) # Test the data import  
        #print(result.has_errors())  
        if not result.has_errors():  
            categoria_resource.import_data(dataset, dry_run=False) # Actually import now  
    return render(request, 'carga_produccion/importar.html')