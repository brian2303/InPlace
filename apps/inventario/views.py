from django.shortcuts import render

# Create your views here.

def index_inventario(request):
    return render(request,'inventario/index.html')