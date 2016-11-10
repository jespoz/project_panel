# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-02 16:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=100, verbose_name=b'm\xc3\xb3dulo')),
            ],
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created'], 'verbose_name': 'Proyecto', 'verbose_name_plural': 'Proyectos'},
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name=b'Asignado a'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'creado el'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, verbose_name=b'descripci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(null=True, verbose_name=b'vencimiento'),
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=b'ult. modificado'),
        ),
        migrations.AlterField(
            model_name='task',
            name='module',
            field=models.CharField(blank=True, max_length=100, verbose_name=b'M\xc3\xb3dulo'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.PositiveIntegerField(choices=[(1, b'Bajo'), (2, b'Medio'), (3, b'Alto')], default=1, verbose_name=b'Prioridad'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'proyecto'),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, b'Proyecto'), (2, b'Tarea'), (3, b'Desarrollo'), (4, b'Presentaci\xc3\xb3n')], default=1, verbose_name=b'Tipo'),
        ),
    ]