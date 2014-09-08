# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0003_auto_20140908_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='pdf_url',
            field=models.URLField(blank=True),
        ),
    ]
