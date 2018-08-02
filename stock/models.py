from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


# Create your models here.

class Cultivo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Campaña(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creacion =  models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre de la campaña', help_text='Ejemplo: Soja Primavera 2018')
    cultivo = models.ForeignKey('Cultivo', on_delete=models.SET_NULL, blank=True, null=True)
    lote = models.ForeignKey('Lote', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    hectareas = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre



class TipoActividad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de actividad'
        verbose_name_plural = "Tipo de actividades"


class Actividad(TimeStampedModel):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    campaña = models.ForeignKey('Campaña', on_delete=models.CASCADE)
    tipo = models.ForeignKey('TipoActividad', on_delete=models.SET_NULL, blank=True, null=True)
    descripcion = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.descripcion


    class Meta:
        verbose_name_plural = "actividades"


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50, help_text='Ej: Semilla, fertilizante, herbicida, etc')


    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, help_text='Ej: Bidon x 20l, Hora, etc')


    def __str__(self):
        return self.nombre


class Producto(TimeStampedModel):
    """
    Este es la tabla que describe insumo o producidho o servicios con su precio actual
    """
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey('CategoriaProducto', null=True, on_delete=models.SET_NULL)
    unidad_medida = models.ForeignKey('UnidadMedida', null=True, on_delete=models.SET_NULL)
    precio_peso = models.DecimalField(max_digits=12, decimal_places=3)
    precio_dolar = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return self.nombre

class Transaccion(TimeStampedModel):

    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=6, decimal_places=3)
    descripcion = models.TextField(null=True, blank=True)
    es_inicial = models.BooleanField(default=False, help_text='Calcular stock a partir de esta cantidad')
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)
    precio_peso = models.DecimalField(max_digits=12, decimal_places=3)
    precio_dolar = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = "Transacciones"
