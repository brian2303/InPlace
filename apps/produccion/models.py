from django.db import models
from datetime import datetime

# Create your models here.

class CategoriaProductos(models.Model):
    nombre_categoria=models.CharField(max_length=25)
    
    class Meta:
        verbose_name='categoria'
        verbose_name_plural='categorias'
        db_table='categoria_productos'
    
    def __str__(self):
        return self.nombre_categoria
        

class Productos(models.Model):
    nombre=models.CharField(max_length=25)
    cantidad=models.CharField(max_length=11)
    precio_unitario=models.DecimalField(max_digits=15, decimal_places=2)
    categoria=models.ForeignKey(
        CategoriaProductos,
        on_delete=models.CASCADE,
        related_name='productos'
        )

    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        db_table='productos'



