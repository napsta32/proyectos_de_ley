from django.test import TestCase, Client


class TestSearchAdvancedViews(TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/search-advanced/')
        self.assertEqual(200, response.status_code)
