# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0009_remove_proyecto_congresistas_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='grupo_parlamentario',
            field=models.CharField(max_length=250, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='iniciativas_agrupadas',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='nombre_comision',
            field=models.CharField(max_length=250, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='numero_de_ley',
            field=models.CharField(max_length=200, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='proponente',
            field=models.CharField(max_length=250, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='titulo_de_ley',
            field=models.CharField(max_length=400, default='', blank=True),
            preserve_default=True,
        ),
    ]
