from django.test import TestCase

from pdl.models import Proyecto
from seguimientos import utils


class SimpleTest(TestCase):
    def test_get_proyecto_from_short_url(self):
        short_url = "4zhube"
        expected = {
            "numero_proyecto": "02764/2013-CR",
            "codigo": "02764",
            "titulo": "Propone Ley Universitaria",
        }
        b = Proyecto(short_url=short_url, numero_proyecto="02764/2013-CR",
                     codigo="02764", titulo="Propone Ley Universitaria",
                     fecha_presentacion="2013-10-10",)
        b.save()
        result = utils.get_proyecto_from_short_url(short_url)
        self.assertEqual(expected['codigo'], result.codigo)

