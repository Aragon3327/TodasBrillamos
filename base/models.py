
# Backend
# Clases que se guardaran en la base de datos
# Docs: https://docs.djangoproject.com/en/5.1/topics/db/models/

from django.db import models

# Modelo de Categorías
class Categorias(models.Model):
    nombre = models.CharField(max_length=255)

# Modelo de items.
class Items(models.Model):
    nombre = models.CharField(max_length=255)
    stock = models.IntegerField()
    precio = models.FloatField()
    descuento = models.FloatField()
    descripción = models.TextField()
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL,null=True)
    