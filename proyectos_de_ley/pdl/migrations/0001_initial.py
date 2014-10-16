# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('codigo', models.CharField(max_length=20)),
                ('numero_proyecto', models.CharField(max_length=50)),
                ('short_url', models.CharField(max_length=20)),
                ('congresistas', models.TextField(blank=True)),
                ('fecha_presentacion', models.DateField(blank=True)),
                ('titulo', models.TextField(blank=True)),
                ('expediente', models.URLField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
                ('seguimiento_page', models.URLField(blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_edited', models.DateTimeField(auto_now=True)),
                ('proponente', models.CharField(default='', blank=True, max_length=250)),
                ('grupo_parlamentario', models.CharField(default='', blank=True, max_length=250)),
                ('iniciativas_agrupadas', models.TextField(default='', blank=True)),
                ('nombre_comision', models.CharField(default='', blank=True, max_length=250)),
                ('titulo_de_ley', models.TextField(default='', blank=True)),
                ('numero_de_ley', models.CharField(default='', blank=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
