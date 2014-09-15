# -*- encoding: utf-8 -*-
import json
import os

from bs4 import BeautifulSoup

from django.test import Client
from django.test import TestCase

from pdl.models import Proyecto
from pdl.models import Slug


class SimpleTest(TestCase):
    def test_proyect_items(self):
        this_folder = os.path.abspath(os.path.dirname(__file__))
        dummy_db_json = os.path.join(this_folder, 'dummy_db.json')
        dummy_items = json.loads(open(dummy_db_json, 'r').read())
        b = Proyecto(**dummy_items[0])
        b.save()

        c = Client()
        response = c.get('/sitemap.xml')
        soup = BeautifulSoup(response.content)
        self.assertEqual(1, len(soup.find_all('url')))

        nombre = 'Zerillo Bazalar, Manuel Salvador'
        slug = 'zerillo_bazalar_manuel/'
        b = Slug(nombre=nombre, slug=slug)
        b.save()
        response = c.get('/sitemap.xml')
        self.assertTrue(slug.encode('utf-8') in response.content)
