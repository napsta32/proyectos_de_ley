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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('codigo', models.CharField(max_length=20)),
                ('numero_proyecto', models.CharField(max_length=50)),
                ('short_url', models.CharField(max_length=20)),
                ('congresistas', models.TextField(blank=True)),
                ('fecha_presentacion', models.DateField()),
                ('titulo', models.TextField(blank=True)),
                ('expediente', models.URLField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
                ('seguimiento_page', models.URLField(blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_edited', models.DateTimeField(auto_now=True)),
                ('proponente', models.TextField(default='', blank=True, null=True)),
                ('grupo_parlamentario', models.TextField(default='', blank=True)),
                ('iniciativas_agrupadas', models.TextField(default='', blank=True, null=True)),
                ('nombre_comision', models.TextField(default='', blank=True, null=True)),
                ('titulo_de_ley', models.TextField(default='', blank=True, null=True)),
                ('numero_de_ley', models.TextField(default='', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('ascii', models.CharField(help_text='nombre sin caracteres escpeciales', max_length=200)),
                ('slug', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='expedientes',
            name='proyecto',
            field=models.ForeignKey(to='pdl.Proyecto'),
        ),
    ]
