import datetime

from django.core.management.base import BaseCommand

from pdl.models import Proyecto


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fix_pdl_fecha_presentacion()

    def fix_pdl_fecha_presentacion(self):
        """This field should be date not datetime.
        """
        projects = Proyecto.objects.all()

        for project in projects:
            try:
                fecha_presentacion = datetime.datetime.strptime(
                    project.fecha_presentacion, '%Y-%m-%d %H:%M:%S+00')
            except ValueError:
                continue

            project.fecha_presentacion = fecha_presentacion.date()
            project.save()
