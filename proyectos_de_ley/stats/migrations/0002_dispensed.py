# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispensed',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('total_approved', models.IntegerField(help_text='Number of projects approved in any instance.')),
                ('total_dispensed', models.IntegerField(help_text='Number of projects that did not go to 2nd round of votes.')),
                ('dispensed_by_plenary', models.IntegerField(help_text='Those projects dispensed due to `acuerdo del pleno`.')),
                ('dispensed_by_spokesmen', models.IntegerField(help_text='Those projects dispensed due to `junta de portavoces`.')),
                ('dispensed_others', models.IntegerField(help_text='All other projects dispensed, and those with no specific reason.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
