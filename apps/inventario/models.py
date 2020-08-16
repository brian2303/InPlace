from django.db import models
from datetime import datetime

# Create your models here.

# Modelo Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=25,verbose_name='Nombres Proveedor')
    ciudad = models.CharField(max_length=25,verbose_name='Ciudad')
    direccion = models.CharField(max_length=50,verbose_name='Dirección')

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'

# Modelo telefono proveedor
class TelefonoProveedor(models.Model):
    numero_telefono = models.CharField(max_length=12,verbose_name='Telefono Proveedor')
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_telefono
    
    class Meta:
        verbose_name = 'Telefono proveedor'
        verbose_name_plural = 'Telefonos proveedor'
        db_table = 'telefono_proveedor'


# Modelo Unidad Medida
class UnidadMedida(models.Model):

    nombre_unidad = models.CharField(max_length=25)
    abreviatura = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'unidades de medida'
        db_table = 'unidad_medida'

    def __str__(self):
        return self.abreviatura


class Insumos(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_minima = models.DecimalField(max_digits=5, decimal_places=2)
    unidad_medida = models.ForeignKey(UnidadMedida,on_delete=models.CASCADE)