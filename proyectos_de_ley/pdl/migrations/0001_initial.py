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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('codigo', models.CharField(max_length=20)),
                ('numero_proyecto', models.CharField(max_length=50)),
                ('short_url', models.CharField(max_length=20)),
                ('congresistas', models.TextField(blank=True)),
                ('fecha_presentacion', models.DateField(null=True)),
                ('titulo', models.TextField(blank=True)),
                ('expediente', models.URLField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
                ('seguimiento_page', models.URLField(blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_edited', models.DateTimeField(auto_now=True)),
                ('proponente', models.CharField(max_length=250, blank=True, default='')),
                ('grupo_parlamentario', models.CharField(max_length=250, blank=True, default='')),
                ('iniciativas_agrupadas', models.TextField(blank=True, default='')),
                ('nombre_comision', models.CharField(max_length=250, blank=True, default='')),
                ('titulo_de_ley', models.TextField(blank=True, default='')),
                ('numero_de_ley', models.CharField(max_length=200, blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=200)),
                ('ascii', models.CharField(max_length=200, help_text='nombre sin caracteres escpeciales')),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='expedientes',
            name='proyecto',
            field=models.ForeignKey(to='pdl.Proyecto'),
        ),
    ]
