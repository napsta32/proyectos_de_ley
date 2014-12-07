import datetime

from django.test import TestCase, Client

from pdl.models import Proyecto
from stats.models import Dispensed


class TestStatsViews(TestCase):
    def setUp(self):
        Proyecto.objects.create(**{
            'numero_proyecto': '02764',
            'time_created': datetime.datetime.now(),
            'fecha_presentacion': '2010-10-10',
        })
        Dispensed.objects.create(**{
            'total_approved': 1444,
            'total_dispensed': 864,
            'dispensed_by_plenary': 23,
            'dispensed_by_spokesmen': 12,
            'dispensed_others': 11,
        })

    def test_index(self):
        c = Client()
        response = c.get('/stats/')
        self.assertEqual(200, response.status_code)
