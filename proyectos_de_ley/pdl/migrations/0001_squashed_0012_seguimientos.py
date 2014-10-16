# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    replaces = [('pdl', '0001_initial'), ('pdl', '0002_proyecto_seguimiento_page'), ('pdl', '0003_auto_20140908_1730'), ('pdl', '0004_auto_20140908_1946'), ('pdl', '0005_auto_20140910_0514'), ('pdl', '0006_proyecto_congresistas_slug'), ('pdl', '0007_auto_20140912_2008'), ('pdl', '0008_slug'), ('pdl', '0009_remove_proyecto_congresistas_slug'), ('pdl', '0010_auto_20140922_1547'), ('pdl', '0011_auto_20140922_1601'), ('pdl', '0012_seguimientos')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='seguimiento_page',
            field=models.URLField(blank=True, default=datetime.date(2014, 9, 7)),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='proyecto',
            old_name='link_to_pdf',
            new_name='expediente',
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='pdf_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='expediente',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='congresistas',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_presentacion',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='titulo',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='grupo_parlamentario',
            field=models.CharField(blank=True, default='', max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='iniciativas_agrupadas',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='nombre_comision',
            field=models.CharField(blank=True, default='', max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='numero_de_ley',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='proponente',
            field=models.CharField(blank=True, default='', max_length=250),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='titulo_de_ley',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
