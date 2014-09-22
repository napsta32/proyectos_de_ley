# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdl', '0011_auto_20140922_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seguimientos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField(blank=True)),
                ('evento', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(to='pdl.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
