from django.shortcuts import render

# Create your views here.

def index_usuarios(request):
    return render(request,'usuarios/index.html')