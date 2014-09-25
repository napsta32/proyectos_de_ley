# -*- encoding: utf-8 -*-
import codecs
from datetime import date
import os

from bs4 import BeautifulSoup

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

    def test_is_law(self):
        codigo = '00002'
        # save an item to our test database
        item = {
            'codigo': '00002',
            'seguimiento_page': 'dummy',
            'fecha_presentacion': date.today(),
        }
        b = Proyecto(**item)
        b.save()

        this_folder = os.path.abspath(os.path.dirname(__file__))
        html_folder = os.path.join(this_folder, 'update_seguimientos')
        html_file = os.path.join(html_folder, codigo + '.html')
        with codecs.open(html_file, 'r', 'latin-1') as f:
            soup = BeautifulSoup(f.read())

        # save its seguimientos
        events = self.cmd.get_seguimientos(soup)
        self.cmd.save_seguimientos(events, codigo)

        # check if it is law so that we don't need to update it
        result = self.cmd.is_law(codigo)
        self.assertEqual(True, result)
