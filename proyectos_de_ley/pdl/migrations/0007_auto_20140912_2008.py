# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0006_proyecto_congresistas_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='congresistas',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='congresistas_slug',
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
    ]
