from django.db import models
from datetime import datetime

class Usuarios(models.Model):
    nombres = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=50)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    estatus = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
class Venta(models.Model):
    cliente_nombre = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=datetime.now)
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    estatus = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)


