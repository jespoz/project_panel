from .models import CabeceraActividad
from django.db.models import Count


def actividades(request):
    return {
        'estados': CabeceraActividad.objects.values(
            'estado__estado', 'estado_id', 'actividad__publico').filter(
            actividad__publico=True).annotate(
            total=Count('estado_id')),
        'public_list': CabeceraActividad.objects.all().filter(
            actividad__publico=True).order_by('estado_id', 'area_id')
    }
