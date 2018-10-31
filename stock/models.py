from django.db import models
from django.urls import reverse
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

    def get_absolute_url(self):
        return reverse('campaña_detalle', args=[self.id])

    def __str__(self):
        return self.nombre


class Lote(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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

    def get_absolute_url(self):
        return reverse(
            'actividad_detalle',
            kwargs=dict(
                id_campaña=self.campaña.id,
                id_actividad=self.id
            )
        )

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
    Este es la tabla que describe insumo o producido o servicios con su precio actual
    """
    nombre        = models.CharField(max_length=50)
    categoria     = models.ForeignKey('CategoriaProducto', null=True, on_delete=models.SET_NULL)
    unidad_medida = models.ForeignKey('UnidadMedida', null=True, on_delete=models.SET_NULL, help_text='Ingresar nombre abreviado.')
    precio_peso   = models.DecimalField(max_digits=12, decimal_places=3, help_text='Precio neto unitario según unidad de medida.')
    precio_dolar  = models.DecimalField(max_digits=12, decimal_places=3, help_text='Precio en dólares según la cotización del día.')
    es_cosechable = models.BooleanField(default=False, help_text='Es resultado del producido de una campaña ?')

    def __str__(self):
        return f'{self.nombre} x {self.unidad_medida}'


class TipoMovimiento(models.Model):
    tipo = models.CharField(max_length=50, help_text='Ej: compra, venta')
    aumenta = models.BooleanField(default=True)

    def __str__(self):
        'Muestra el nombre del objeto'
        return self.tipo


class Movimiento(TimeStampedModel):
    OPC_TC = Choices(('001', 'Factura A'), ('004', 'Recibos A'),
                     ('006', 'Factura B'), ('009', 'Recibos B'),
                     ('011', 'Factura C'), ('015', 'Recibos C'),
                     ('017', 'Liq.Serv.Publ.A'), ('018', 'Liq.Serv.Publ.B'),
                     ('033', 'Liq.Prim.de Granos'), ('089', 'Resumen de datos')
                    )
    OPC_LETRA = Choices('A', 'B', 'C', 'M', 'E', 'X')

    producto    = models.ForeignKey('Producto', on_delete=models.CASCADE)
    tipo        = models.ForeignKey('TipoMovimiento', on_delete=models.CASCADE)
    cantidad    = models.DecimalField(max_digits=12, decimal_places=3)
    descripcion = models.TextField(null=True, blank=True)
    fecha       = models.DateTimeField()
    es_inicial  = models.BooleanField(default=False, help_text='Calcular stock a partir de esta cantidad')
    actividad   = models.ForeignKey('Actividad', on_delete=models.CASCADE)
    precio_peso = models.DecimalField(max_digits=12, decimal_places=3)
    precio_dolar= models.DecimalField(max_digits=12, decimal_places=3)
    tipo_comp   = models.CharField(choices=OPC_TC, default='OPC_TC.089', max_length=3, verbose_name='Tipo de comprobante')
    letra_comp  = models.CharField(choices=OPC_LETRA, default=OPC_LETRA.X, max_length=1, verbose_name='Letra')
    pto_venta   = models.IntegerField(verbose_name='Punto de venta')
    nro_comp    = models.IntegerField(verbose_name='Número de comprobante')

    def __str__(self):
        return f'{self.tipo}: {self.producto} ({self.cantidad} {self.producto.unidad_medida})'


    def save(self, *args, **kwargs):
        """Sobrecarga del metodo que se encarga de guardar el estado
        actual de la instancia Movimiento (a nivel python) a la
        base de datos.

        Antes de efectivamente guardar, calculamos si el valor cantidad debe
        ser positivo o negativo en funcion del tipo de movimiento
        """
        if not self.tipo.aumenta:
            self.cantidad = - abs(self.cantidad)
        else:
            self.cantidad = abs(self.cantidad)
        super().save(*args, **kwargs)
