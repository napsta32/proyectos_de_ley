# -*- encoding: utf-8 -*-
import json
import os

from bs4 import BeautifulSoup

from django.test import Client
from django.test import TestCase

from pdl.models import Proyecto


class SimpleTest(TestCase):
    def test_feed(self):
        c = Client()
        response = c.get('/rss.xml')
        soup = BeautifulSoup(response.content)
        expected = 'Proyectos de ley emitidos por el Congreso de la ' \
                   'República del Perú'
        self.assertEqual(expected, soup.title.get_text())

        this_folder = os.path.abspath(os.path.dirname(__file__))
        dummy_db_json = os.path.join(this_folder, 'dummy_db.json')
        dummy_items = json.loads(open(dummy_db_json, 'r').read())
        b = Proyecto(**dummy_items[0])
        b.save()
        response = c.get('/rss.xml')
        soup = BeautifulSoup(response.content)
        self.assertEqual(1, len(soup.find_all('item')))
