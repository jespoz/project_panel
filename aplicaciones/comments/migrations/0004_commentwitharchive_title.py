# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20160811_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentwitharchive',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
