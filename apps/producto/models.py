from uuid import uuid4

from django.db import models

class Categoria(models.Model):
    uuid=models.UUIDField(unique=True,editable=False,default=uuid4)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class Producto(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    nombre = models.CharField(max_length=150, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
