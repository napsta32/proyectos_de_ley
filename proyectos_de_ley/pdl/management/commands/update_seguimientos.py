"""Custom command to run weekly. It goes through all `proyectos` in our
database and looks of new events in the `seguimiento_page`. It tries to
update our database with new `seguimiento` events for each `proyecto`."""
from optparse import make_option

from django.core.management.base import BaseCommand

from pdl.management.commands.scraper import Command as ScraperCommand
from pdl.models import Proyecto, Seguimientos


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

            if self.is_law(i.codigo) is True:
                self.stdout.write('Nothing to update for %s.' % str(i.codigo))
            else:
                soup = self.get(i.seguimiento_page)
                events = self.get_seguimientos(soup)

                self.save_seguimientos(events, codigo)

                if options['test'] is True:
                    break

    def is_law(self, codigo):
        """Check if this project is already a `law` in our database model
        Seguimiento.

        :param codigo:
        :return: True or False
        """
        proyecto = Proyecto.objects.filter(codigo=codigo)[0]
        items = Seguimientos.objects.filter(proyecto=proyecto)

        promulgado, publicado = False, False
        for i in items:
            if 'promulgado' in i.evento.lower():
                promulgado = True
            if 'publicado' in i.evento.lower():
                publicado = True

        if promulgado is True and publicado is True:
            return True
        else:
            return False
