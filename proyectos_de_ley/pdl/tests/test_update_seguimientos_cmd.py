# -*- encoding: utf-8 -*-
from datetime import date

from django.test import TestCase

from pdl.management.commands.update_seguimientos import Command
from pdl.models import Proyecto
from pdl.models import Seguimientos


class USeguimientosTest(TestCase):
    def setUp(self):
        self.cmd = Command()
        self.maxDiff = None

    def test_handle(self):
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'no_color': False, 'full_scrapping': False, 'verbosity': '1',
            'traceback': None, 'tor': False, 'debug': True, 'test': True,
            'pythonpath': None
        }

        # save an item to our test database
        item = {
            'codigo': '03774',
            'seguimiento_page': 'http://www2.congreso.gob.pe/Sicr/TraDocEst'
                                'Proc/CLProLey2011.nsf/Sicr/TraDocEstProc/C'
                                'LProLey2011.nsf/PAporNumeroInverso/9609130'
                                'B9871582F05257D4A00752301?opendocument',
            'fecha_presentacion': date.today(),
        }
        b = Proyecto(**item)
        b.save()

        seguimientos = Seguimientos.objects.all()
        self.assertEqual(len(seguimientos), 0)

        self.cmd.handle(self, *args, **options)
        seguimientos = Seguimientos.objects.all()
        self.assertGreater(len(seguimientos), 1)
