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
        return f'{self.fecha} -- {self.usuario.username}'

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


class Pago(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='pago')
    mercado_pago_order_id = models.CharField(max_length=100, blank=True, null=True)
    mercado_pago_payment_id = models.CharField(max_length=100, blank=True, null=True)
    qr_data = models.TextField(blank=True, null=True)
    qr_url= models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago de {self.venta.uuid} - {self.estado}"
