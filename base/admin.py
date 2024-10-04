
# Backend
# Modelos que puede manipular el admin

from django.contrib import admin
from .models import Item,Categoria,Usuario,Pedido

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Usuario)
