# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 15:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0015_tipousuario_usuarioactividad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarioactividad',
            name='actividad',
        ),
        migrations.RemoveField(
            model_name='usuarioactividad',
            name='tipoUsuario',
        ),
        migrations.RemoveField(
            model_name='usuarioactividad',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='usuarioactividad',
            name='usuario_asignado',
        ),
        migrations.DeleteModel(
            name='TipoUsuario',
        ),
        migrations.DeleteModel(
            name='UsuarioActividad',
        ),
    ]
