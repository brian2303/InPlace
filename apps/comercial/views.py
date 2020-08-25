from django.shortcuts import render

# Create your views here.

def index_comercial(request):
    return render(request,'clientes/index.html')