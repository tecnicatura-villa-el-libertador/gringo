from django.shortcuts import render
from django.db.models import Sum
from .models import Movimiento, Producto, Campaña, CategoriaProducto

from django.shortcuts import render, redirect
from .forms import FilterForm


# Create your views here.
def stock(request):
    tabla = {}
    for p in Producto.objects.all():
        # buscamos el movimiento inicial mas nuevo, o el primero que exista
        inicial = p.movimiento_set.filter(
            es_inicial=True
        ).order_by('-fecha').first() or p.movimiento_set.order_by('fecha').first()
        
        if not inicial:
            # si no hay movimientos, el stock para este producto es 0
            tabla[p] = 0
            continue

        # filtramos todos los movimientos asociados al producto posteriores al inicial
        contables = p.movimiento_set.filter(fecha__gte=inicial.fecha)
        # sumamos  cantidades a partir del movimiento incial
        total = contables.aggregate(total=Sum('cantidad'))['total']
        tabla[p] = total
    return render(request, 'stock/stock.html', {'tabla': tabla})

def campaña(request):
    tabla = {}
    for cmp in Campaña.objects.all():
        # Datos de la campaña...
        # calcular cantidad*precio_peso, cantidad*precio_dolar
        total = Movimiento.objects.filter(
                actividad__campaña=cmp
            ).aggregate(total_pesos=Sum('precio_peso'), 
                        total_dolares=Sum('precio_dolar'))


        tabla[cmp] = total
    return render(request, 'stock/campaña.html', {'tabla': tabla})


def mov_gral (request):
    tabla  = Movimiento.objects.all()
    formfilter = FilterForm(request.GET)
    if formfilter.is_valid():
        orden = formfilter.cleaned_data.pop('orden')
        for clave, valor in formfilter.cleaned_data.items(): #recorre las opciones de filtrado.
            if not valor:   # filtra cada opcion seleccionada.
                continue
            tabla  = tabla.filter(**{clave: valor}) # Los ** convierten el dicc a un string con sus valores corresp.        
    if orden:
        tabla = tabla.order_by(orden)
    return render(request, 'stock/mov_gral.html', {'form': formfilter, 'object_list': tabla})


from django.views.generic.list import ListView


class MovListView(ListView):

    model = Movimiento
    paginate_by = 5  # if pagination is desired
    template_name = 'stock/mov_gral.html'