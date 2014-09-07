# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='seguimiento_page',
            field=models.URLField(default=datetime.date(2014, 9, 7), blank=True),
            preserve_default=False,
        ),
    ]
