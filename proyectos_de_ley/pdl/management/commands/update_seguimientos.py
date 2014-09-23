"""Custom command to run weekly. It goes through all `proyectos` in our
database and looks of new events in the `seguimiento_page`. It tries to
update our database with new `seguimiento` events for each `proyecto`."""

from django.core.management.base import NoArgsCommand, CommandError

from pdl.models import Proyecto


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        proyectos = Proyecto.objects.all()
        for i in proyectos:
            print(i.codigo, i.seguimiento_page)