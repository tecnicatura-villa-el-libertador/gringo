from django.shortcuts import render
from django.db.models import Sum
from .models import Movimiento, Producto


# Create your views here.
def stock(request):
	tabla = {}
	for p in Producto.objects.all():
		# buscamos el movimiento inicial mas nuevo, o el primero que exista
		inicial = p.movimiento_set.filter(
			es_inicial=True
		).order_by('-fecha').first() or p.movimiento_set.order_by('-fecha').first()
		
		if not inicial:
			# si no hay movimientos, el stock para este producto es 0
			tabla[p] = 0
			continue

		# filtramos todos los movimientos asociados al producto posteriores al inicial
		nuevos = p.movimiento_set.filter(fecha__gt=inicial.fecha)
		import ipdb
		ipdb.set_trace()
		# sumamos cantidad inicial mas la sumatoria de cantidades de los nuevos movimientos
		cantidad_nuevos = nuevos.aggregate(total=Sum('cantidad'))['total']
		if not cantidad_nuevos:
			cantidad_nuevos = 0
		total = inicial.cantidad + cantidad_nuevos
		tabla[p] = total
	return render(request, 'stock/stock.html', {'tabla': tabla})