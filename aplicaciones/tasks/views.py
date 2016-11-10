# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  TemplateView, View)
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.db.models import Count, Sum

from braces.views import (LoginRequiredMixin, StaffuserRequiredMixin,
                          StaticContextMixin, JSONResponseMixin)
from django_tables2.views import SingleTableView

from .models import Task
from .tables import TaskTable
from aplicaciones.new_task.models import CabeceraActividad, Costo

import json
import datetime

now = datetime.datetime.now().date()


class BaseListTasksView(LoginRequiredMixin,  SingleTableView):
    """
    The base view that can list all tasks. Other actual view will apply just
    filters on this.
    """
    model = Task
    table_class = TaskTable
    filters = {}
    exclude_filters = {}

    def get_queryset(self):
        """
        Exclude completed tasks from normal listing.
        """
        queryset = super(BaseListTasksView, self).get_queryset()
        if self.filters:
            queryset = queryset.filter(**self.filters)
        if self.exclude_filters:
            queryset = queryset.exclude(**self.exclude_filters)
        return queryset.select_related('assigned_user')


class ListTasksView(BaseListTasksView):
    exclude_filters = {'status': Task.STATUS_CHOICES.complete}

    def get_context_data(self, **kwargs):
        context = super(ListTasksView, self).get_context_data(**kwargs)
        context['private_list'] = CabeceraActividad.objects.all().filter(
            actividad__publico=False,
            actividad__usuario=self.request.user).order_by('estado_id')
        print context['private_list']
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


class ListIncompleteTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list just incomplete tasks.
    """
    filters = {'status': Task.STATUS_CHOICES.incomplete}
    static_context = {"incomplete_menu": True}


class ListUnReviewedTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list only the tasks that are ready to be reviewed
    """
    filters = {'status': Task.STATUS_CHOICES.ready_for_review}
    static_context = {"unreviewed_menu": True}


class ListStandByTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list only the tasks that are completed.
    """
    filters = {'status': Task.STATUS_CHOICES.stand_by}
    static_context = {"standby_menu": True}


class ListCompletedTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list only the tasks that are completed.
    """
    filters = {'status': Task.STATUS_CHOICES.complete}
    static_context = {"completed_menu": True}


class CreateTaskView(LoginRequiredMixin, CreateView):
    """
    View to create new tasks.
    """
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('list_tasks')

    def post(self, request, *args, **kwargs):
        """
        Overriding default method to add support of cancel button.
        """
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse_lazy('list_tasks'))
        return super(CreateTaskView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding default functionality for saving the user who created the
        task.
        """
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('list_tasks'))


class DetailTaskView(LoginRequiredMixin, DetailView):
    """
    View to show the details of a task.
    """
    model = Task


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    View to update existing task.
    """
    model = Task
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        """
        Overriding to handle cancel button.
        """
        if 'cancel' in request.POST:
            self.object = self.get_object()
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateTaskView, self).post(request, *args, **kwargs)


class SetTaskReadyView(LoginRequiredMixin, View):
    """
    View to set a task ready for review.
    """

    def post(self, request, *args, **kwargs):
        """
        Set the task as ready for review.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.ready_for_review
        task.completed_at = timezone.now()
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskIncompleteView(LoginRequiredMixin, View):
    """
    View to set a task back to incomplete
    """

    def post(self, request, *args, **kwargs):
        """
        View to set a task as not ready for review.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.incomplete
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskStandByView(LoginRequiredMixin, View):
    """
    View to set a task back to incomplete
    """

    def post(self, request, *args, **kwargs):
        """
        View to set a task as not ready for review.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.stand_by
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskCompletedView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    """
    View to set a task as completed
    """
    raise_exception = True

    def post(self, request, *args, **kwargs):
        """
        View to set a task as completed.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.complete
        task.reviewed_by = request.user
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class ReportHomeView(LoginRequiredMixin, TemplateView):
    """
    View to render template for report home view
    """
    template_name = 'tasks/report.html'

    def get_context_data(self, **kwargs):
        """
        Adding some data to the context
        """
        context = super(ReportHomeView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        incomplete_tasks = tasks.filter(
            status=Task.STATUS_CHOICES.incomplete)
        unreviewed_tasks = tasks.filter(
            status=Task.STATUS_CHOICES.ready_for_review)
        standby_tasks = tasks.filter(
            status=Task.STATUS_CHOICES.stand_by)
        completed_tasks = tasks.filter(
            status=Task.STATUS_CHOICES.complete)
        context['incomplete_task_count'] = incomplete_tasks.count()
        context['unreviewed_tasks_count'] = unreviewed_tasks.count()
        context['completed_tasks'] = completed_tasks.count()
        context['standby_tasks'] = standby_tasks.count()
        context['report_menu'] = True
        return context


class TasksJsonView(LoginRequiredMixin, JSONResponseMixin, View):
    """
    Returns the task by its status
    """

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        tasks_by_status = (
            tasks.values('status'
                         ).annotate(count=Count('status')
                                    ).order_by('-count'))
        for item in tasks_by_status:
            item['label'] = Task.STATUS_CHOICES[item.get('status')]
            item['data'] = item.get('count')
            del item['status']
            del item['count']
        task_by_module = (
            tasks.values('module'
                         ).annotate(count=Count('module')
                                    ).order_by('-count'))
        for item in task_by_module:
            item['label'] = item.get('module')
            item['data'] = item.get('count')
            del item['module']
            del item['count']
        response = {
            'task_by_status': list(tasks_by_status),
            'task_by_module': list(task_by_module)
        }
        return self.render_json_response(response)


def pie_actividades(request):
    context = []
    color = ''
    if request.is_ajax():
        data = CabeceraActividad.objects.values(
            'estado__estado', 'estado_id').filter(
            actividad__publico=True).annotate(
            cant=Count('actividad_id')).order_by('-estado_id')
        for x in data:
            if x['estado_id'] == 1:
                color = '#d9534f'
            if x['estado_id'] == 2:
                color = '#F0AD4E'
            if x['estado_id'] == 3:
                color = '#5cb85c'
            if x['estado_id'] == 4:
                color = '#5bc0de'
            context.append({
                'name': x['estado__estado'],
                'data': x['cant'],
                'color': color
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def bar_encurso(request):
    context = []
    if request.is_ajax():
        data = CabeceraActividad.objects.values(
            'actividad__nombre', 'inicio', 'vencimiento').filter(
            estado_id=2, actividad__publico=True)
        for x in data:
            data1 = (now - x['inicio']).days
            if x['vencimiento']:
                data2 = (x['vencimiento'] - x['inicio']).days
            else:
                data2 = 0
            if data2 != 0:
                cumpl = (float(data1) / float(data2)) * 100
            else:
                cumpl = 0
            context.append({
                'name': x['actividad__nombre'],
                'data': cumpl
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def bar_terminada(request):
    context = []
    if request.is_ajax():
        data = CabeceraActividad.objects.values(
            'actividad__nombre', 'inicio', 'vencimiento', 'terminado').filter(
            estado_id=3, actividad__publico=True)
        for x in data:
            data1 = (x['vencimiento'] - x['inicio']).days
            data2 = (x['terminado'] - x['inicio']).days
            cumpl = (float(data1) / float(data2)) * 100
            # if cumpl > 130:
            #     cumpl = 130
            context.append({
                'name': x['actividad__nombre'],
                'data': cumpl
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def get_areas(request):
    context = []
    if request.is_ajax():
        data = CabeceraActividad.objects.values(
            'area__short', 'area_id').filter(
            estado_id=request.POST['id'],
            actividad__publico=request.POST['publico']).annotate(
            total=Count('area_id')).order_by('area__short')
        for x in data:
            context.append({
                'id': x['area_id'],
                'area': x['area__short']
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def get_projects(request):
    context = []
    if request.is_ajax():
        if request.POST['id']:
            data = CabeceraActividad.objects.values(
                'actividad__nombre', 'actividad_id').filter(
                estado_id=request.POST['estado'],
                actividad__publico=request.POST['publico'],
                area_id=request.POST['id']).annotate(
                total=Count('area_id')).order_by('actividad__nombre')
        else:
            data = CabeceraActividad.objects.values(
                'actividad__nombre', 'actividad_id').filter(
                estado_id=request.POST['estado'],
                actividad__publico=request.POST['publico'],
                area_id=None).annotate(
                total=Count('area_id')).order_by('actividad__nombre')
        for x in data:
            context.append({
                'id': x['actividad_id'],
                'actividad': x['actividad__nombre']
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')


def get_projects_table(request):
    context = []
    if request.is_ajax():
        data = Costo.objects.values('actividad__actividad__nombre',
                                    'actividad__actividad_id').filter(
            actividad__area_id=request.POST['id']).annotate(
            sumCosto=Sum('costo'))
        for x in data:
            context.append({
                'costo': x['sumCosto'],
                'actividad': x['actividad__actividad__nombre'],
                'id': x['actividad__actividad_id']
            })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data, content_type='application/json')
