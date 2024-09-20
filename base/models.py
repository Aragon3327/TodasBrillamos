
# Backend
# Clases que se guardaran en la base de datos
# Docs: https://docs.djangoproject.com/en/5.1/topics/db/models/

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Regex
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número de teléfono debe cumplir con el formato: '+999999999'. Solo se permiten números con 15 digitos.")

    # Variables personalizadas
    email = models.EmailField(null=True, blank=True,unique=True)
    nombre = models.CharField(null=True,blank=True,max_length=550)
    es_admin = models.BooleanField(default=False)
    direccion = models.TextField(null=True,blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # OtrosS
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nombre

# Modelo de Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nombre

# ruta_items = FileSystemStorage(location='/media/items')

# Modelo de items.
class Item(models.Model):
    nombre = models.CharField(max_length=255)
    stock = models.IntegerField()
    precio = models.FloatField()
    descuento = models.FloatField(null=True,blank=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL,null=True)
    imagen = models.ImageField(upload_to="items",null=True,blank=True)
    def __str__(self) -> str:
        return self.nombre
    
    
class Pedido(models.Model):
    entregado = models.BooleanField(default=False)
    
    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL,null=True)
    total = models.FloatField(null=True,blank=True)

    items = models.ManyToManyField(Item,related_name='items')
