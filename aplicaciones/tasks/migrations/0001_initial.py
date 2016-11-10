# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-01 19:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('due_date', models.DateField(null=True)),
                ('module', models.CharField(blank=True, max_length=100)),
                ('priority', models.PositiveIntegerField(choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')], default=1)),
                ('type', models.PositiveIntegerField(choices=[(1, b'Bug'), (2, b'Enhancement'), (3, b'Task'), (4, b'Proposal')], default=3)),
                ('status', models.PositiveIntegerField(choices=[(1, b'Incomplete'), (2, b'Ready for Review'), (3, b'Complete')], default=1, editable=False)),
                ('completed_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('assigned_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name=b'Assigned To')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('reviewed_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]