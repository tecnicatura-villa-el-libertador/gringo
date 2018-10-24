import os

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseForbidden
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from .models import Movimiento, Producto, Campaña, CategoriaProducto,Lote
from .models import Movimiento, Producto, Actividad, Movimiento, Campaña, CategoriaProducto
from .forms import FilterForm, MovimientoModelForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CampañaCreate(LoginRequiredMixin, CreateView):
    model = Campaña
    fields = ['nombre', 'cultivo', 'lote']

    def form_valid(self, form):
        campaña = form.save(commit=False)
        campaña.usuario = self.request.user
        campaña.save()
        return redirect('/')


class LoteCreate(LoginRequiredMixin, CreateView):
    model = Lote
    fields = ['nombre', 'descripcion', 'latitud', 'longitud', 'hectareas']

    def form_valid(self, form):
        lote = form.save(commit=False)
        lote.usuario = self.request.user
        lote.save()
        return redirect('/')


@login_required
def campaña_detalle(request, id):
    campaña = get_object_or_404(Campaña, id=id)
    #if campaña.usuario != request.user:
    #    return HttpResponseForbidden()
    return render(request, 'stock/campaña_detalle.html', {'campaña': campaña})


class ActividadCreate(LoginRequiredMixin, CreateView):
    model = Actividad
    fields = ['fecha_inicio', 'fecha_fin', 'tipo', 'descripcion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaña'] = get_object_or_404(Campaña, id=self.kwargs['id'])
        return context

    def form_valid(self, form):
        actividad = form.save(commit=False)
        actividad.campaña = get_object_or_404(Campaña, id=self.kwargs['id'])
        actividad.save()
        return redirect(actividad)


@login_required
def actividad_detalle(request, id_campaña, id_actividad):
    campaña = get_object_or_404(Campaña, id=id_campaña)
    if campaña.usuario != request.user:
        return HttpResponseForbidden()
    actividad = get_object_or_404(Actividad, campaña=campaña, id=id_actividad)
    form = MovimientoModelForm(request.POST if request.method == 'POST' else None)
    if form.is_valid():
        mov = form.save(commit=False)
        mov.actividad = actividad
        mov.save()
        return redirect(actividad)

    return render(request, 'stock/actividad_detalle.html', {
        'campaña': campaña,
        'actividad': actividad,
        'form': form,
    })


@login_required
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
def campañas_listado(request):
    tabla = {}
    for cmp in Campaña.objects.all():
        # Datos de la campaña...
        # calcular cantidad*precio_peso, cantidad*precio_dolar
        total = Movimiento.objects.filter(
            actividad__campaña=cmp
        ).aggregate(total_pesos=Sum('precio_peso'),
                    total_dolares=Sum('precio_dolar'))
        tabla[cmp] = total
    return render(request, 'stock/campañas_listado.html', {'tabla': tabla})


@login_required
def lote(request):
    tabla = {}
    for cmp in Lote.objects.all():
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
    if request.user.is_authenticated:
        # si el usuario ya está logueado, no le mostramos el landing page
        return redirect('resumen_campañas')
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
