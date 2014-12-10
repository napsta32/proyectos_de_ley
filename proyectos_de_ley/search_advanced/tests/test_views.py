from django.test import TestCase, Client


class TestSearchAdvancedViews(TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/search-advanced/')
        self.assertEqual(200, response.status_code)

    def test_index_form_invalid(self):
        c = Client()
        response = c.get('/search-advanced/?date_from=hola&date_to=12%2F19%2F2014')
        self.assertEqual(200, response.status_code)
