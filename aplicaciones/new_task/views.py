from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, View
from braces.views import (LoginRequiredMixin)
from .forms import ActividadForm
from .models import CabeceraActividad, Tareas, Comentarios, TipoActividad
from .models import UsuariosActividad, Costo, Area
from django.db.models import Count, Sum

import datetime
import json
import os

now = datetime.datetime.now().date()


class CrearActividad(LoginRequiredMixin, CreateView):
    form_class = ActividadForm
    template_name = "tasks/task_list.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CrearActividad, self).get_context_data(**kwargs)
        context['private_list'] = CabeceraActividad.objects.all().filter(
            actividad__publico=False,
            actividad__usuario=self.request.user).order_by('estado_id')
        new_data = Costo.objects.values('actividad__area_id').annotate(
            costo=Sum('costo')).order_by('-costo')
        context['resumen'] = []
        context['total_act'] = 0
        context['total_cost'] = 0
        for x in new_data:
            costo = 0
            data = CabeceraActividad.objects.values(
                'area__area', 'area_id').filter(
                actividad__publico=True,
                area_id=x['actividad__area_id']).annotate(
                total=Count('actividad_id'))
            for i in data:
                costo += x['costo']
                context['resumen'].append({
                    'area': i['area__area'],
                    'cantidad': i['total'],
                    'costo': x['costo'],
                    'id': i['area_id']
                })
                context['total_act'] += i['total']
            context['total_cost'] += costo
        data = CabeceraActividad.objects.values(
            'actividad__nombre', 'inicio', 'vencimiento', 'terminado').filter(
            estado_id=3, actividad__publico=True)
        suma = 0
        cuenta = 0
        for x in data:
            data1 = (x['vencimiento'] - x['inicio']).days
            data2 = (x['terminado'] - x['inicio']).days
            suma += (float(data1) / float(data2)) * 100
            cuenta += 1
        if float(cuenta) == 0:
            cumpl = 0
        else:
            cumpl = float(suma) / float(cuenta)
        if cumpl > 130:
            context['cumpl_total'] = 130
        else:
            context['cumpl_total'] = round(cumpl, 0)
        return context


class UpdateActividad(LoginRequiredMixin, DetailView):
    model = CabeceraActividad
    template_name = "new_task/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateActividad, self).get_context_data(**kwargs)
        context['hoy'] = now
        context['tasks'] = Tareas.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['comments'] = Comentarios.objects.all().filter(
            actividad_id=self.kwargs.get('pk')).order_by('-id')[:4]
        context['users'] = User.objects.all()
        context['types'] = TipoActividad.objects.all()
        context['users_activity'] = UsuariosActividad.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['costs_activity'] = Costo.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['costo_total'] = 0
        for x in context['costs_activity']:
            context['costo_total'] = context['costo_total'] + x.costo
        medias = Comentarios.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['medias_context'] = []
        context['medias'] = Comentarios.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['areas'] = Area.objects.all()
        for x in medias:
            name, extension = os.path.splitext(x.adjunto.name)
            context['medias_context'].append({
                'extension': extension.replace(".", ""),
                'archivo': x.adjunto.name
            })
        indicadores = CabeceraActividad.objects.all().filter(
            actividad_id=self.kwargs.get('pk'))
        context['restantes'] = 0
        for x in indicadores:
            if x.inicio:
                if x.terminado:
                    data1 = (x.terminado - x.inicio).days
                else:
                    data1 = (now - x.inicio).days
                if x.vencimiento:
                    data2 = (x.vencimiento - x.inicio).days
                    if data1 == 0:
                        cumplimiento = 100
                    else:
                        if x.terminado:
                            cumplimiento = (float(data2) / float(data1)) * 100
                        else:
                            cumplimiento = (float(data1) / float(data2)) * 100
                    context['cumplimiento'] = int(round(cumplimiento, 0))
                    context['restantes'] = data2 - data1
        return context


class SetEnCursoView(View):

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(CabeceraActividad, pk=self.kwargs.get('pk'))
        task.inicio = now
        task.estado_id = 2
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskView(View):

    def post(self, request, *args, **kwargs):
        checked = True
        if request.POST['complete'] == 'true':
            checked = False
        task = get_object_or_404(Tareas, pk=request.POST['id'])
        task.completado = checked
        task.save()
        return HttpResponseRedirect(None)


class SetTerminadoView(View):

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(CabeceraActividad, pk=self.kwargs.get('pk'))
        task.terminado = now
        task.estado_id = 3
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


def load_more_comments(request):
    context = []
    if request.is_ajax():
        data = Comentarios.objects.all().filter(
            id__lt=request.POST['last'],
            actividad_id=request.POST['id']).order_by('-id')[:3]
        for x in data:
            context.append({
                'id': x.id,
                'usuario': x.usuario.username,
                'comentario': x.comentario,
                'creado': x.creado.strftime('%d de %B de %Y a las %H:%M'),
                'adjunto': str(x.adjunto)
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def send_comment(request):
    id = request.POST['id']
    if 'file' in request.FILES:
        file = request.FILES['file']
    else:
        file = ''
    comment = Comentarios()
    comment.actividad_id = id
    comment.comentario = request.POST['comentario']
    comment.adjunto = file
    comment.usuario_id = request.user.id
    comment.save()
    task = get_object_or_404(CabeceraActividad, pk=id)
    return HttpResponseRedirect(task.get_absolute_url())


def change_assigned(request):
    if request.is_ajax():
        task = get_object_or_404(CabeceraActividad, pk=request.POST['id'])
        task.asignado_id = request.POST['user_assigned']
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


def area_assigned(request):
    if request.is_ajax():
        task = get_object_or_404(CabeceraActividad, pk=request.POST['id'])
        task.area_id = request.POST['area_assigned']
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


def type_assigned(request):
    if request.is_ajax():
        task = get_object_or_404(CabeceraActividad, pk=request.POST['id'])
        task.tipo_id = request.POST['type_assigned']
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


def change_espired(request):
    if request.is_ajax():
        task = get_object_or_404(CabeceraActividad, pk=request.POST['id'])
        task.vencimiento = request.POST['date']
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


def insert_new_user(request):
    id = request.POST['id']
    context = []
    if request.is_ajax():
        funciones = request.POST['descripcion']
        modelo = UsuariosActividad()
        modelo.actividad_id = id
        modelo.usuario_asigando = request.POST['usuario']
        modelo.funciones = funciones
        modelo.usuario_id = request.user.id
        modelo.save()
    data = UsuariosActividad.objects.values(
        'usuario_asigando', 'funciones').filter(actividad_id=id)
    for x in data:
        context.append({
            'usuario_asigando': x['usuario_asigando'],
            'funciones': x['funciones']
        })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def insert_new_cost(request):
    id = request.POST['id']
    context = []
    if request.is_ajax():
        item = request.POST['item']
        modelo = Costo()
        modelo.actividad_id = id
        modelo.costo = request.POST['costo']
        modelo.item = item
        modelo.usuario_id = request.user.id
        modelo.save()
    data = Costo.objects.values(
        'item', 'costo').filter(actividad_id=id)
    for x in data:
        context.append({
            'item': x['item'],
            'costo': x['costo']
        })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def insert_new_task(request):
    id = request.POST['id']
    context = []
    if request.is_ajax():
        task = Tareas()
        task.actividad_id = id
        task.tarea = request.POST['task']
        task.usuario_id = request.user.id
        task.save()
    data = Tareas.objects.values(
        'id', 'tarea', 'completado').filter(actividad_id=id)
    for x in data:
        if x['completado']:
            bool = 'true'
        else:
            bool = 'false'
        context.append({
            'id': x['id'],
            'tarea': x['tarea'],
            'completado': bool
        })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')
