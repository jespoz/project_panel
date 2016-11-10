# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Task, Module


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass
