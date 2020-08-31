from django.db import models
from datetime import datetime

# ==== modelos para crear el crud de provedores ==== #

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


# ==== modelos para crear el crud de insumos con su unidad de medida ====

"""modelo de unidad_medida"""
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=25)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'unidad_medida'
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'unidades de medida'


"""modelo de insumos"""
class Insumos(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=0)
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        default='sin categoria',
        on_delete=models.SET_DEFAULT,
    )

    class Meta:
        db_table = 'insumos'
        verbose_name = 'insumo'
        verbose_name_plural='insumos'

