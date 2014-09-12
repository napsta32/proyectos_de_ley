# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0005_auto_20140910_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='congresistas_slug',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
