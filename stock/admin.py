from django.contrib import admin
from stock.models import (
    Cultivo, Campaña, TipoActividad, Actividad,
    CategoriaProducto, Producto, UnidadMedida,
    Transaccion
)


class CampañaAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'cultivo', 'usuario')
    list_filter = ('cultivo',)



class ActividadAdmin(admin.ModelAdmin):

    list_display = ('tipo', 'descripcion', 'fecha_inicio', 'fecha_fin')
    list_filter = ('tipo', 'fecha_inicio')


admin.site.register(Campaña, CampañaAdmin)

admin.site.register(Actividad, ActividadAdmin)


for m in (
        Cultivo, TipoActividad,
        CategoriaProducto, Producto, UnidadMedida,
        Transaccion):
    admin.site.register(m)

