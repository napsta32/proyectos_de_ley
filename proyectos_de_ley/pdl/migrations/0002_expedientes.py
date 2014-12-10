# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expedientes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('pdf_url', models.URLField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
