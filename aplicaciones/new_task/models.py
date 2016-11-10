# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import models


class Registro(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)

    class Meta:
        abstract = True


class Actividad(Registro):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    publico = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Actividades'

    def __unicode__(self):
        return self.nombre


class TipoActividad(models.Model):
    tipo = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Tipos de Actividades'

    def __unicode__(self):
        return self.tipo


class Estado(models.Model):
    estado = models.CharField(max_length=50)

    def __unicode__(self):
        return self.estado


class Area(models.Model):
    area = models.CharField(max_length=50)
    short = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.area


class CabeceraActividad(models.Model):
    actividad = models.OneToOneField(Actividad, primary_key=True)
    estado = models.ForeignKey(Estado)
    asignado = models.ForeignKey(User, null=True, blank=True, default=None)
    inicio = models.DateField(null=True, blank=True)
    tipo = models.ForeignKey(TipoActividad, null=True, blank=True)
    vencimiento = models.DateField(null=True, blank=True)
    terminado = models.DateField(null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cabecera de Actividades'

    def get_absolute_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.actividad.nombre


class Tareas(Registro):
    actividad = models.ForeignKey(Actividad)
    tarea = models.CharField(max_length=100)
    completado = models.BooleanField(default=False)


class Comentarios(Registro):
    actividad = models.ForeignKey(Actividad)
    comentario = models.TextField()
    adjunto = models.FileField(upload_to='comment/')


class UsuariosActividad(Registro):
    actividad = models.ForeignKey(Actividad)
    usuario_asigando = models.CharField(max_length=50)
    funciones = models.CharField(max_length=200, null=True, blank=True)


class Costo(models.Model):
    actividad = models.ForeignKey(CabeceraActividad)
    item = models.CharField(max_length=50)
    costo = models.FloatField()
