from django.urls import path
from apps.correos.views import request_email

urlpatterns = [
    path('',request_email,name='envio_email'),
]