# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0008_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabeceraactividad',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='new_task.Estado'),
            preserve_default=False,
        ),
    ]
