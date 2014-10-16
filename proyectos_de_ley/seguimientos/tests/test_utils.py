from django.test import TestCase

from pdl.models import Proyecto
from seguimientos import utils


class Object(object):
    """Dummy class for testing."""
    pass


class SimpleTestSeguimientos(TestCase):
    def test_get_proyecto_from_short_url(self):
        short_url = "4zhube"
        expected = {
            "numero_proyecto": "02764/2013-CR",
            "codigo": "02764",
            "titulo": "Propone Ley Universitaria",
            "iniciativas_agrupadas": ['01790', '01800'],
        }
        b = Proyecto(short_url=short_url, numero_proyecto="02764/2013-CR",
                     codigo="02764", titulo="Propone Ley Universitaria",
                     fecha_presentacion="2013-10-10",
                     iniciativas_agrupadas="{01790,01800}")
        b.save()
        result = utils.get_proyecto_from_short_url(short_url)
        self.assertEqual(expected['codigo'], result.codigo)
        self.assertEqual(expected['iniciativas_agrupadas'],
                         result.iniciativas_agrupadas)

    def test_prepare_json_for_d3(self):
        b = Proyecto(short_url="4zhube", numero_proyecto="02764/2013-CR",
                     codigo="02764", titulo="Propone Ley Universitaria",
                     fecha_presentacion="2013-10-10",
                     iniciativas_agrupadas="{01790,01800}")
        b.save()

        item = Object()
        item.numero_proyecto = "02764/2013-CR"
        item.codigo = "02764"
        item.titulo = "Propone Ley Universitaria"
        item.iniciativas_agrupadas = ['02764']

        expected = {'nodes': [{'codigo': '02764', 'url': '/p/4zhube'}]}
        result = utils.prepare_json_for_d3(item)
        self.assertEqual(expected, result)


