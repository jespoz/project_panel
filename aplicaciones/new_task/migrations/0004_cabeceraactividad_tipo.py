# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0003_tipoactividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabeceraactividad',
            name='tipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='new_task.TipoActividad'),
            preserve_default=False,
        ),
    ]
