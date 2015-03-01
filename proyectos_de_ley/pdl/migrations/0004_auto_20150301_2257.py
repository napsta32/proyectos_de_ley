# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0003_auto_20150301_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_presentacion',
            field=models.DateTimeField(null=True),
        ),
    ]
