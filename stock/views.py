import os

from django.shortcuts import render, redirect
from django.db.models import Sum
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from .models import Movimiento, Producto, Campaña, CategoriaProducto
from .forms import FilterForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView


class CampañaCreate(CreateView):
    model = Campaña
    fields = ['nombre', 'cultivo', 'lote']

    def form_valid(self, form):
        campaña = form.save(commit=False)
        campaña.usuario = self.request.user
        campaña.save()
        return redirect('/')


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

@login_required
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


@login_required
def mov_gral (request):
    tabla = Movimiento.objects.all()
    if request.method == 'GET':
        formfilter = FilterForm(request.GET)

    if formfilter.is_valid():
        orden = formfilter.cleaned_data.pop('orden')
        for clave, valor in formfilter.cleaned_data.items(): #recorre las opciones de filtrado.
            # si el formulario de filtro es valido (por ahora cualquier configuracion lo es)
            # entonces los "datos enviados y limpios" se iteran para aplicarlos iterativamente
            # como filtros.
            # Para esto se usa el "desempacado de parametros" (**kwargs)
            # que es una forma de pasar parametros nombrados a partir de un diccionario

            if not valor:   # filtra cada opcion seleccionada.
                continue
            tabla = tabla.filter(**{clave: valor}) # Los ** convierten el dicc a un string con sus valores corresp.
    else:
        formfilter = FilterForm()
    if orden:
        tabla = tabla.order_by(orden)

    return render(request, 'stock/mov_gral.html', {'form': formfilter, 'object_list': tabla})

def inicio(request):
    return render(request, 'stock/landing.html')

@login_required
def actividades(request):
    return render(request, 'stock/actividades.html')


@login_required
def download_db(request):
    filename = settings.DATABASES['default']['NAME']
    response = HttpResponse(open(filename, 'rb').read(), content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)
    return response
