"""Custom command to run weekly. It goes through all `proyectos` in our
database and looks of new events in the `seguimiento_page`. It tries to
update our database with new `seguimiento` events for each `proyecto`."""
from optparse import make_option

from django.core.management.base import BaseCommand

from pdl.management.commands.scraper import Command as ScraperCommand
from pdl.models import Proyecto


class Command(ScraperCommand):
    """Need some inherited methods from our scraper class."""
    option_list = BaseCommand.option_list + (
        make_option('--test',
                    action='store_true',
                    dest='test',
                    default=False,
                    help='Use when running tests to stop after one iteration.',
                    ),
    )
    def handle(self, *args, **options):
        self.tor = False
        self.mysocket = ""

        proyectos = Proyecto.objects.all()
        for i in proyectos:
            codigo = i.codigo
            soup = self.get(i.seguimiento_page)
            events = self.get_seguimientos(soup)

            self.save_seguimientos(events, codigo)

            if options['test'] is True:
                break
