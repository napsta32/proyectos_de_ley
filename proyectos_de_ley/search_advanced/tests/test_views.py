import json
import os

from django.test import TestCase, Client

from pdl.models import Proyecto
from pdl.models import Seguimientos


class TestSearchAdvancedViews(TestCase):
    def setUp(self):
        self.maxDiff = None

        this_folder = os.path.abspath(os.path.dirname(__file__))
        dummy_db_json = os.path.join(this_folder, '..', '..', 'pdl', 'tests', 'dummy_db.json')
        dummy_items = json.loads(open(dummy_db_json, 'r').read())

        for i in dummy_items:
            b = Proyecto(**i)
            b.save()
            s = Seguimientos(proyecto=b, fecha='2014-06-23',
                             evento='Decreado a... Ciencia, Innovación y Tecnología')
            s.save()

    def test_index(self):
        c = Client()
        response = c.get('/search-advanced/')
        self.assertEqual(200, response.status_code)

    def test_index_form_invalid(self):
        c = Client()
        response = c.get('/search-advanced/?date_from=hola&date_to=12%2F19%2F2014')
        self.assertEqual(200, response.status_code)

    def test_index_search_date(self):
        c = Client()
        response = c.get('/search-advanced/?date_from=03%2F03%2F2015&date_to=07%2F02%2F2015')
        self.assertEqual(200, response.status_code)

    def test_index_search_comission(self):
        c = Client()
        response = c.get('/search-advanced/?comision=Ciencia')
        self.assertTrue('arco y flecha' in str(response.content))
