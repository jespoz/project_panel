# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 19:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0019_auto_20160913_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariosactividad',
            old_name='funciones',
            new_name='descripcion',
        ),
    ]
