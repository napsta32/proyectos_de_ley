# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0002_expedientes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_presentacion',
            field=models.DateField(null=True),
        ),
    ]
