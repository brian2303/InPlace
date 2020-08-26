from django.db import models

# Create your models here.

"""modelo de cliente"""
class Cliente(models.Model):

    numero_identificacion = models.CharField(max_length=15)
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


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