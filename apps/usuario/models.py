from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    dni=models.CharField(max_length=9,unique=True)

    def __str__(self):
        return f'{self.username} -- { self.dni}'
