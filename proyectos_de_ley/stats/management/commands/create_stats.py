"""
This command queries the pdl_seguimientos table to calculate some statictics
for `/stats` page. These stat values go to tables for this app.

* projects that are being accumulated in each `comisión`.
* projects that were aproved without 2nd round of votes.
"""
import datetime
import re

from django.core.management.base import BaseCommand, CommandError

from pdl.models import Seguimientos
from stats.models import ComisionCount
from stats.models import Dispensed


class Command(BaseCommand):
    help = 'Parses the table `pdl_seguimientos` and creates a summary table ' \
           'containing `En Comision` events for each proyecto, only if this ' \
           'is the last event for them.'

    def handle(self, *args, **options):
        queryset = Seguimientos.objects.all()

        # There are 24 `comisiones` in total
        comisiones = set()
        for i in queryset:
            # res = re.match("(en\s+comisión(\s\w+,*)+)", i.evento, re.I)
            res = re.match("(en\s+comisión(\s\w+)+)", i.evento, re.I)
            if res:
                this_comision = re.sub("En\s+comisión\s+", "", res.groups()[0])
                this_comision = re.sub("\s+y\s+.+", "", this_comision)
                comisiones.add(this_comision)

        queryset = Seguimientos.objects.order_by('proyecto_id', '-fecha')
        comisiones_count = {}

        this_proyecto_id = ''
        for i in queryset:
            if i.proyecto_id != this_proyecto_id:
                for comision in comisiones:
                    if comision in i.evento:
                        if comision not in comisiones_count:
                            comisiones_count[comision] = 0
                        comisiones_count[comision] += 1
            this_proyecto_id = i.proyecto_id

        for k, v in comisiones_count.items():
            ComisionCount.objects.update_or_create(
                comision=k, defaults={'count': v},
            )

        # Get projects that did not go to 2da round of votes
        self.get_dispensed_projects()

    def get_dispensed_projects(self):
        total_approved = Seguimientos.objects.filter(evento__icontains='aprobado').count()
        total_dispensed = Seguimientos.objects.filter(evento__icontains='dispensado 2da').count()
        dispensed_by_plenary = Seguimientos.objects.filter(
            evento__icontains='dispensado 2da').filter(evento__icontains='pleno').count()
        dispensed_by_spokesmen = Seguimientos.objects.filter(
            evento__icontains='dispensado 2da').filter(evento__icontains='portavoces').count()
        dispensed_others = total_dispensed - dispensed_by_plenary - dispensed_by_spokesmen

        Dispensed.objects.update_or_create(
            total_approved=total_approved,
            total_dispensed=total_dispensed,
            dispensed_by_plenary=dispensed_by_plenary,
            dispensed_by_spokesmen=dispensed_by_spokesmen,
            dispensed_others=dispensed_others,
        )
