from django.contrib import admin
from stock.models import (
    Cultivo, Campaña, TipoActividad, Actividad,
    CategoriaProducto, Producto, UnidadMedida,
    Movimiento, Lote, TipoMovimiento
)


class CampañaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'cultivo')
    list_filter = ('cultivo',)

class MovimientoInline(admin.StackedInline):
    model = Movimiento

class ActividadAdmin(admin.ModelAdmin):

    list_display = ('tipo', 'descripcion', 'fecha_inicio', 'fecha_fin')
    list_filter = ('tipo', 'fecha_inicio')

    inlines = [
        MovimientoInline,
    ]


admin.site.register(Campaña, CampañaAdmin)
admin.site.register(Actividad, ActividadAdmin)


for m in (
        Cultivo, TipoActividad,
        CategoriaProducto, Producto, UnidadMedida,
        Lote, TipoMovimiento):
    admin.site.register(m)


























