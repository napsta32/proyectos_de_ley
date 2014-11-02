import json

from django.test import TestCase, Client

from pdl.models import Proyecto, Seguimientos


class TestViews(TestCase):
    def setUp(self):
        b = Proyecto(**{
            'codigo': '00586',
            'numero_proyecto': '00586/2011-CR',
            'fecha_presentacion': '2010-10-10',
            'short_url': '4huj5x',
            'id': 1,
            }
        )
        b.save()

        Seguimientos.objects.create(**{
            'fecha': '2011-01-01',
            'evento': "Decretado a... Trabajo y Seguridad Social",
            'proyecto': b,
            }
        )
        Seguimientos.objects.create(**{
            'fecha': '2012-02-02',
            'evento': "En comisi\u00f3n Trabajo y Seguridad Social",
            'proyecto': b,
            }
        )

    def test_index(self):
        c = Client()
        response = c.get('/api/seguimientos/4huj5x', follow=True)
        as_string = response.content.decode("utf-8")
        as_dict = json.loads(as_string)
        self.assertEqual('Proyecto No: 00586_2011-CR',
                         as_dict['timeline']['text'])
