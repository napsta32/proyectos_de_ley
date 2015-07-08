# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slug',
            name='ascii',
            field=models.CharField(default='', help_text='nombre sin caracteres escpeciales', max_length=200),
            preserve_default=False,
        ),
    ]
