import unittest
from django.test import Client
from bs4 import BeautifulSoup


class SimpleTest(unittest.TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/')
        soup = BeautifulSoup(response.content)
        result = soup.find_all('h1')[0].get_text()
        self.assertEqual('Proyectos de Ley', result)