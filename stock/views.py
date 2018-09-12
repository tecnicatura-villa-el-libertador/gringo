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
	if request.method == 'POST':
		formfilter = FilterForm(request.POST)
		if formfilter.is_valid():
			return render(request, 'stock/mov_gral.html', {'form': formfilter})
	else:
		formfilter = FilterForm()
		#query   = Movimiento.objects.all().filter()	
		#querytp = CategoriaProducto.objects.all()
		return render(request, 'stock/mov_gral.html', {'form': formfilter})





