# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seguimientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeguimientosJson',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('headline', models.TextField(blank=True)),
                ('codigo', models.TextField(blank=True)),
                ('date', models.TextField(blank=True)),
                ('type', models.TextField(blank=True)),
                ('text', models.TextField(blank=True)),
                ('timeline', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
