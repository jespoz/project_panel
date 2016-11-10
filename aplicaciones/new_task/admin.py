from django.contrib import admin
from .models import *


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    pass


@admin.register(TipoActividad)
class TipoActividadAdmin(admin.ModelAdmin):
    pass


@admin.register(CabeceraActividad)
class CabeceraActividadAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass
