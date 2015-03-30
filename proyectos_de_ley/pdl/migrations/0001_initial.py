# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expedientes',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('codigo', models.CharField(max_length=20)),
                ('numero_proyecto', models.CharField(max_length=50)),
                ('short_url', models.CharField(max_length=20)),
                ('congresistas', models.TextField(blank=True)),
                ('fecha_presentacion', models.DateTimeField(null=True)),
                ('titulo', models.TextField(blank=True)),
                ('expediente', models.URLField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
                ('seguimiento_page', models.URLField(blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_edited', models.DateTimeField(auto_now=True)),
                ('proponente', models.CharField(blank=True, default='', max_length=250)),
                ('grupo_parlamentario', models.CharField(blank=True, default='', max_length=250)),
                ('iniciativas_agrupadas', models.TextField(blank=True, default='')),
                ('nombre_comision', models.CharField(blank=True, default='', max_length=250)),
                ('titulo_de_ley', models.TextField(blank=True, default='')),
                ('numero_de_ley', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='expedientes',
            name='proyecto',
            field=models.ForeignKey(to='pdl.Proyecto'),
            preserve_default=True,
        ),
    ]
