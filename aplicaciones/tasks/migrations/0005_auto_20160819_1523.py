# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20160811_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name=b'vencimiento'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, b'Listo para revisi\xc3\xb3n'), (2, b'Incomplete'), (3, b'Complete'), (4, b'stand_by')], default=1, editable=False),
        ),
    ]