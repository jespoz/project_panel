# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 20:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('new_task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabeceraActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField(null=True)),
                ('actividad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='new_task.Actividad')),
                ('asignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]