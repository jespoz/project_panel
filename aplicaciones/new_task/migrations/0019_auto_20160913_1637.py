# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0018_auto_20160913_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariosactividad',
            name='funciones',
            field=models.TextField(),
        ),
    ]
