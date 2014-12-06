import datetime
import re

from django.core.management.base import BaseCommand, CommandError

from pdl.models import Seguimientos
from stats.models import ComisionCount


class Command(BaseCommand):
    help = 'Parses the table `pdl_seguimientos` and creates a summary table ' \
           'containing `En Comision` events for each proyecto, only if this ' \
           'is the last event for them.'

    def handle(self, *args, **options):
        queryset = Seguimientos.objects.all()

        # There are 24 `comisiones` in total
        comisiones = set()
        for i in queryset:
            res = re.match("(en\s+comisión(\s\w+,*)+)", i.evento, re.I)
            if res:
                comisiones.add(res.groups()[0])

        queryset = Seguimientos.objects.order_by('proyecto_id', '-fecha').distinct('proyecto_id')
        comisiones_count = {}
        for i in queryset:
            for comision in comisiones:
                if comision in i.evento:
                    if comision not in comisiones_count:
                        comisiones_count[comision] = 0
                    comisiones_count[comision] += 1
        for k, v in comisiones_count.items():
            obj, created = ComisionCount.objects.update_or_create(
                comision=k, count=v
            )
