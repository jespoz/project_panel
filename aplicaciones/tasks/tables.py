# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2.utils import A

from .models import Task


STATUS_SYMBOL_MAP = {
    Task.STATUS_CHOICES.complete: 'ok',
    Task.STATUS_CHOICES.incomplete: 'minus-sign',
    Task.STATUS_CHOICES.ready_for_review: 'bell',
    Task.STATUS_CHOICES.stand_by: 'eye-close'
}

PRIORTY_BADGE_MAP = {
    Task.PRIORITY_CHOICES.bajo: '',
    Task.PRIORITY_CHOICES.medio: 'alert-warning',
    Task.PRIORITY_CHOICES.alto: 'alert-danger'
}


class TaskTable(tables.Table):
    id = tables.LinkColumn('task_detail', args=[A('pk')])
    created = tables.Column(visible=True)

    def render_created(self, value, record):
        return mark_safe(value.strftime("%d-%m-%Y"))

    def render_last_modified(self, value, record):
        return mark_safe(value.strftime("%d-%m-%Y"))

    def render_due_date(self, value, record):
        return mark_safe(value.strftime("%d-%m-%Y"))

    def render_assigned_user(self, value):
        """
        Show full name if available.
        """
        return value.get_full_name() or value

    def render_priority(self, value, record):
        """
        Give different coloured badges to different priority.
        """
        badge = PRIORTY_BADGE_MAP.get(record.priority)
        return mark_safe("<span class='badge {}'>{}</span>".format(badge, value))

    def render_status(self, value, record):
        """
        Show icons instead of show status display text.
        """
        symbol_html = "<span class='glyphicon glyphicon-{}'></span>"
        # Using record.status as `value` will contain the get_status_display()
        # result.
        symbol_html = symbol_html.format(STATUS_SYMBOL_MAP[record.status])
        return mark_safe(symbol_html)

    class Meta:
        model = Task
        attrs = {'class': 'table table-condensed rowlink table-striped table-hover', }
        fields = ('id', 'title', 'module',
                  'priority', 'assigned_user', 'type', 'created',
                  'last_modified', 'due_date', 'status')
        order_by = 'due_date'
        per_page = 15
