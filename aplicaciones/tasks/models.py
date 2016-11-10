# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.forms.utils import to_current_timezone

from model_utils import Choices


class TimeStampedModel(models.Model):
    """
    An abstract model for the common fields 'created' and 'last_modified'.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name='creado el')
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name='ult. modificado')

    class Meta:
        abstract = True


class Module(models.Model):
    module = models.CharField(max_length=100, verbose_name='módulo')

    def __unicode__(self):
        return self.module

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


class Task(TimeStampedModel):
    """
    Model that represent a task.
    """
    PRIORITY_CHOICES = Choices((1, 'bajo', 'Bajo'),
                               (2, 'medio', 'Medio'),
                               (3, 'alto', 'Alto'))
    TYPE_CHOICES = Choices((1, 'proyecto', 'Proyecto'),
                           (2, 'tarea', 'Tarea'),
                           (3, 'desarrollo', 'Desarrollo'),
                           (4, 'presentacion', 'Presentación'))
    STATUS_CHOICES = Choices((1, 'ready_for_review', 'Listo para revisión'),
                             (2, 'incomplete', 'Incomplete'),
                             (3, 'complete', 'Complete'),
                             (4, 'stand_by', 'stand_by'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   blank=True,
                                   editable=False,
                                   related_name='tasks')
    title = models.CharField(max_length=255, verbose_name='proyecto')
    description = models.TextField(blank=True, verbose_name='descripción')
    due_date = models.DateField(
        null=True, blank=True, verbose_name='vencimiento')
    module = models.ForeignKey(Module, verbose_name='módulo')
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES,
                                           default=PRIORITY_CHOICES.bajo,
                                           verbose_name='Prioridad')
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      null=True,
                                      blank=True,
                                      verbose_name="Asignado a",
                                      related_name='assigned_tasks')
    type = models.PositiveIntegerField(choices=TYPE_CHOICES,
                                       default=TYPE_CHOICES.proyecto,
                                       verbose_name='Tipo')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES,
                                         default=STATUS_CHOICES.ready_for_review,
                                         editable=False)
    # Time at which user submitted it for review
    completed_at = models.DateTimeField(null=True,
                                        blank=True,
                                        editable=False)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True,
                                    blank=True,
                                    editable=False,
                                    related_name='reviewed_tasks')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def is_due(self):
        """
        Return True if this task crossed due date, otherwise false.
        """
        # Convert to current tz, otherwise we are comparing with utc. the date
        # will be entered respect to our current tz
        date_now = to_current_timezone(timezone.now()).date()
        if not self.is_complete() and self.due_date < date_now:
            return True
        else:
            return False

    def is_due_today(self):
        """
        Check if the task due date is today
        """
        date_now = to_current_timezone(timezone.now()).date()
        if self.due_date == date_now:
            return True
        else:
            return False

    def is_complete(self):
        """
        Returns True if the task is marked as completed.
        """
        if self.status == self.STATUS_CHOICES.complete:
            return True
        else:
            return False

    def is_standby(self):
        """
        Returns True if the task is marked as completed.
        """
        if self.status == self.STATUS_CHOICES.stand_by:
            return True
        else:
            return False

    def is_ready_for_review(self):
        """
        Returns True if the task is marked as ready for review.
        """
        if self.status == self.STATUS_CHOICES.ready_for_review:
            return True
        else:
            return False

    def is_incomplete(self):
        """
        Returns True if the task is marked as not completed.
        """
        if self.status == self.STATUS_CHOICES.incomplete:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title
