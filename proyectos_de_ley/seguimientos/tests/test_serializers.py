import datetime

from django.test import TestCase

from seguimientos.serializers import IniciativasSerializer
from seguimientos.serializers import SeguimientosSerializer


class TestSerializers(TestCase):
    def setUp(self):
        self.iniciativa = {
            "nodes": "02764",
            "links": "/p/4zhube",
        }
        self.seguimiento = {
            "headline": "Headline",
            "codigo": "02764",
            "date": "2012-10-12",
            "type": "",
            "text": "",
            "timeline": "",
        }

    def test_iniciativa_serializer(self):
        result = IniciativasSerializer.restore_object('json', self.iniciativa)
        self.assertEqual('02764', result.nodes)

    def test_iniciativa_serializer_instance(self):
        instance = IniciativasSerializer.restore_object('json', self.iniciativa)
        result = IniciativasSerializer.restore_object('json', self.iniciativa, instance=instance)
        self.assertEqual('02764', result.nodes)

    def test_seguimiento_serializer(self):
        result = SeguimientosSerializer.restore_object('json', self.seguimiento)
        self.assertEqual('Headline', result.headline)

    def test_seguimiento_serializer_instance(self):
        instance = SeguimientosSerializer.restore_object('json', self.seguimiento)
        result = SeguimientosSerializer.restore_object('json', self.seguimiento, instance=instance)
        self.assertEqual('Headline', result.headline)
