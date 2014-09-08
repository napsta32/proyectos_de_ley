# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0002_proyecto_seguimiento_page'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proyecto',
            old_name='link_to_pdf',
            new_name='expediente',
        ),
    ]
