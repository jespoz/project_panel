# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 12:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0005_auto_20160823_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipoactividad',
            options={'verbose_name_plural': 'Tipos de Actividades'},
        ),
        migrations.AlterField(
            model_name='cabeceraactividad',
            name='asignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
