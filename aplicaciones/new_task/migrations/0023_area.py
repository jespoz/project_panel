# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_task', '0022_costo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=50)),
            ],
        ),
    ]
