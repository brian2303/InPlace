from django.db import models
from django.forms import model_to_dict
from apps.produccion.models import Productos
from datetime import datetime
# Create your models here.

"""modelo de cliente"""
class Cliente(models.Model):

    numero_identificacion = models.CharField(max_length=15)
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        db_table = "cliente"
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nombres

"""modelo para guardar los telefonos por cliente"""
class TelefonoCliente(models.Model):

    numero_telefono = models.CharField(max_length=20)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name = 'telefonos'
    )

    class Meta:
        db_table = 'telefono_cliente'
        verbose_name = "telefono cliente"
        verbose_name_plural = "telefonos cliente"

    def __str__(self):
        return self.numero_telefono

"""modelo de ventas"""
class Ventas(models.Model):

    ESTADO = (
        ('cotizacion','Cotizacion'),
        ('venta','Venta'),
    )
    
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING) 
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)
    iva = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)
    total = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)
    estado = models.CharField(max_length=10,choices=ESTADO,default="")
    

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['detalle'] = [detalle.toJSON()  for detalle in self.detalleventa_set.all()]
        return item

    class Meta:
        db_table = 'venta_productos'
        verbose_name = "venta producto"
        verbose_name_plural = "ventas productos"

    def __str__(self):
        return str(self.fecha) 


"""modelo de detalle de ventas"""
class DetalleVenta(models.Model):
    producto = models.ForeignKey(Productos,on_delete=models.CASCADE)
    venta = models.ForeignKey(Ventas,on_delete=models.CASCADE)
    precio_venta = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.0,max_digits=9, decimal_places=2)

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['producto'] = self.producto.toJSON()
        item['precio_venta'] = format(self.precio_venta, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'detalle venta'
        verbose_name_plural = 'detalle de ventas'

    def __str__(self):
        return self.producto.nombre
