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
            'iniciativas_agrupadas': '{00001,00002,00586}',
            'titulo_de_ley': 'Titulo de Ley',
            'id': 1,
        })
        b1 = Proyecto(**{
            'codigo': '00001',
            'numero_proyecto': '00001/2011-CR',
            'fecha_presentacion': '2010-10-10',
            'short_url': '4auj5a',
            'id': 2,
        })
        c = Seguimientos(**{
            'fecha': '2012-10-10',
            'evento': 'en comisión Justicia',
            'proyecto': b,
        })
        b.save()
        b1.save()
        c.save()
        call_command('create_stats')

    def test_create_stats(self):
        res = ComisionCount.objects.all()
        expected = 1
        for i in res:
            self.assertEqual(expected, i.count)

    def test_all_iniciativas_with_title_of_law(self):
        res = Proyecto.objects.get(codigo='00001')
        expected = 'Titulo de Ley'
        result = res.titulo_de_ley
        self.assertEqual(expected, result)
