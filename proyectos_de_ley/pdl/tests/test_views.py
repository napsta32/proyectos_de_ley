import json
import os
import unittest

from bs4 import BeautifulSoup

from django.test import Client

from pdl import views
from pdl.models import Proyecto


class SimpleTest(unittest.TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/')
        soup = BeautifulSoup(response.content)
        result = soup.find_all('h1')[0].get_text()
        self.assertEqual('Proyectos de Ley', result)

    def test_get_last_items(self):
        this_folder = os.path.abspath(os.path.dirname(__file__))
        dummy_db_json = os.path.join(this_folder, 'dummy_db.json')
        dummy_items = json.loads(open(dummy_db_json, 'r').read())
        for i in dummy_items:
            b = Proyecto(**i)
            b.save()

        expected = dict(codigo="03774")
        item = views.get_last_items()[0]
        result = dict(codigo=item.codigo)
        self.assertEqual(expected, result)
