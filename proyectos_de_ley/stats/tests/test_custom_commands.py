from django.test import TestCase
from django.core.management import call_command

from pdl.models import Proyecto
from pdl.models import Seguimientos
from stats.models import ComisionCount


class TestCustomCommand(TestCase):
    def setUp(self):
        b = Proyecto(**{
            'codigo': '00586',
            'numero_proyecto': '00586/2011-CR',
            'fecha_presentacion': '2010-10-10',
            'short_url': '4huj5x',
            'id': 1,
        })
        c = Seguimientos(**{
            'fecha': '2012-10-10',
            'evento': 'en comisión Justicia',
            'proyecto': b,
        })
        c.save()

    def test_create_stats(self):
        call_command('create_stats')
        res = ComisionCount.objects.all()
        expected = 1
        for i in res:
            self.assertEqual(expected, i.count)
