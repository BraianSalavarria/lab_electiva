from uuid import uuid4

from django.db import models

from apps.producto.models import Producto
from apps.usuario.models import Usuario


class Venta(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    pago_efectuado = models.BooleanField(default=False,null=True,blank=True)
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.fecha -- self.usuario.nombre}'

class ItemVenta(models.Model):
    venta= models.ForeignKey(Venta,on_delete=models.CASCADE,related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

class RendicionDiaria(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    fecha = models.DateField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_ventas = models.PositiveIntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')