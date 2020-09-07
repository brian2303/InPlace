from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "espanol/contenido.html"

class IndexViewEnglish(TemplateView):
    template_name = "english/content.html"

# Create your views here.
