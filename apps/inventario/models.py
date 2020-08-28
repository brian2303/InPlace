from django.db import models
from datetime import datetime

# Create your models here.

"""modelo de proveedor"""
class Proveedor(models.Model):
    nombre=models.CharField(max_length=25)
    ciudad=models.CharField(max_length=25)
    direccion=models.CharField(max_length=25)
    
    class Meta:
        verbose_name='proveedor'
        verbose_name_plural='proveedores'
        db_table='proveedor'

"""modelo de telefonos del proveedor"""
class TelefonoProveedor(models.Model):
    numero_telefono=models.CharField(max_length=11)
    proveedor=models.ForeignKey(
        Proveedor, 
        on_delete=models.CASCADE, 
        related_name='telefonos'
    )

    class Meta:
        verbose_name='telefono'
        verbose_name_plural='telefonos'
        db_table='telefono_proveedor'
