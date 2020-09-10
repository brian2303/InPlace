from django.db import models
from datetime import datetime
from django.forms import model_to_dict
# ==== modelos para crear el crud de provedores ==== #

"""modelo de proveedor"""
class Proveedor(models.Model):
    nombre=models.CharField(max_length=25)
    ciudad=models.CharField(max_length=25)
    direccion=models.CharField(max_length=25)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name='proveedor'
        verbose_name_plural='proveedores'
        db_table='proveedor'
    
    def __str__(self):
        return self.nombre
    

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

    def toJSON(self):
        item = model_to_dict(self)
        return item

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

    def toJSON(self):
        item = model_to_dict(self)
        item['unidad_medida'] = self.unidad_medida.toJSON()
        return item

    class Meta:
        db_table = 'insumos'
        verbose_name = 'insumo'
        verbose_name_plural='insumos'

# ===== modelos para crear la compra de insumos =====

class CompraInsumos(models.Model):

    proveedor = models.ForeignKey(Proveedor,on_delete=models.DO_NOTHING) 
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)
    iva = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)
    total = models.DecimalField(default=0.0,max_digits=9,decimal_places=2)

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['detalle'] = [detalle.toJSON()  for detalle in self.detallecompra_set.all()]
        return item

    class Meta:
        db_table = 'compra_insumos'
        verbose_name = "compra insumo"
        verbose_name_plural = "compra de insumos"

    def __str__(self):
        return str(self.fecha) 


class DetalleCompra(models.Model):
    insumo = models.ForeignKey(Insumos,on_delete=models.CASCADE)
    compra = models.ForeignKey(CompraInsumos,on_delete=models.CASCADE)
    precio_compra = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.0,max_digits=9, decimal_places=2)

    def toJSON(self):
        item = model_to_dict(self, exclude=['compra'])
        item['insumo'] = self.insumo.toJSON()
        item['precio_compra'] = format(self.precio_compra, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'detalle compra'
        verbose_name_plural = 'detalle de compras'

    def __str__(self):
        return self.insumo.nombre