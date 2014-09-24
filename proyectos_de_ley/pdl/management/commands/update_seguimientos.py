"""Custom command to run weekly. It goes through all `proyectos` in our
database and looks of new events in the `seguimiento_page`. It tries to
update our database with new `seguimiento` events for each `proyecto`."""

from django.core.management.base import BaseCommand, CommandError
from pdl.management.commands.scraper import Command as ScraperCommand

from pdl.models import Proyecto


class Command(ScraperCommand):
    """Inherits some methods from our scraper class."""
    def handle(self, *args, **options):
        self.tor = False

        proyectos = Proyecto.objects.all()
        for i in proyectos:
            codigo = i.codigo
            soup = self.get(i.seguimiento_page)
            events = self.get_seguimientos(soup)

            self.save_seguimientos(events, codigo)
            for j in events:
                print(j)
            break

