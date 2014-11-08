import datetime

from django.test import TestCase, Client

from search_advanced import views



class TestSearchAdvancedViews(TestCase):
    # def setUp(self):
        # Proyecto.objects.create(**{
            # 'numero_proyecto': '02764',
            # 'time_created': datetime.datetime.now(),
            # 'fecha_presentacion': '2010-10-10',
        # })



    def test_index(self):
        c = Client()
        response = c.get('/search-advanced/')
        self.assertEqual(200, response.status_code)
