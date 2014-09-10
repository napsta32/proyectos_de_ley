# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0004_auto_20140908_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='expediente',
            field=models.URLField(blank=True),
        ),
    ]
