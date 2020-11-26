from django.db import models
from datetime import datetime
from django.forms import model_to_dict
# Create your models here.

"""Modelo de Categoría de Productos"""
class CategoriaProductos(models.Model):
    nombre_categoria=models.CharField(max_length=25)
    
    class Meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'
        db_table='categoria_productos'
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.nombre_categoria
        
"""Modelo de Productos"""
class Productos(models.Model):
    nombre=models.CharField(max_length=25)
    cantidad=models.CharField(max_length=11)
    precio_unitario=models.DecimalField(max_digits=15, decimal_places=2)
    categoria=models.ForeignKey(
        CategoriaProductos,
        on_delete=models.CASCADE,
        related_name='productos'
        )

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['precio_unitario'] = format(self.precio_unitario, '.2f')
        return item

    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        db_table='productos'


"""Modelo de Transportadora"""
class Transportadora(models.Model):
    nombre=models.CharField(max_length=25)
    ciudad=models.CharField(max_length=25)
    direccion=models.CharField(max_length=25)
    email=models.CharField(max_length=25)

    class Meta:
        verbose_name='transportadora'
        verbose_name_plural='transportadora'
        db_table='transportadora'
    
    def __str__(self):
        return self.nombre


"""Modelo para guardar los telefonos de la Transportadora"""
class TelefonoTransportadora(models.Model):

    numero_telefono = models.CharField(max_length=15)
    transportadora = models.ForeignKey(
        Transportadora,
        on_delete=models.CASCADE,
        related_name = 'telefonos'
    )

    class Meta:
        db_table = 'telefono_transportadora'
        verbose_name = "telefono transportadora"
        verbose_name_plural = "telefonos transportadoras"

    def __str__(self):
        return self.numero_telefono


"""Modelo de Ordenes de Despacho"""
class OrdenProduccion(models.Model):
    fechaRegistro = models.DateField(default=datetime.now)
    fechaEntrega = models.DateField()
    fechaRecoleccion = models.DateField()    
    ciudad=models.CharField(max_length=25)
    transportadora=models.ForeignKey(
        Transportadora,
        on_delete=models.CASCADE,
        related_name='produccion'
    )

    class Meta:
        verbose_name='orden produccion'
        verbose_name_plural='ordenes produccion'
        db_table='produccion'
    
    def __str__(self):
        return self.ciudad
