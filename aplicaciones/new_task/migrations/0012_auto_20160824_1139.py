# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0011_cabeceraactividad_vencimiento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cabeceraactividad',
            options={'verbose_name_plural': 'Cabecera de Actividades'},
        ),
        migrations.AddField(
            model_name='cabeceraactividad',
            name='terminado',
            field=models.DateField(blank=True, null=True),
        ),
    ]
