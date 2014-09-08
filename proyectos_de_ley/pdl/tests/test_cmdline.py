#-*- encoding: utf-8 -*-
import codecs
from datetime import datetime
import os

from bs4 import BeautifulSoup

from django.test import TestCase
from pdl.management.commands.scraper import Command
from pdl.models import Proyecto


class ScrapperTest(TestCase):
    def setUp(self):
        self.congreso_url = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                       'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
        self.scrapper_cmd = Command()

    def test_tor1(self):
        """If user does not enter argument for tor, it should be True by
        default."""
        options = dict(tor=False, full_scrapping=False)
        self.scrapper_cmd.handle(**options)
        result = self.scrapper_cmd.tor
        expected = False
        self.assertEqual(expected, result)

    def test_tor2(self):
        """If user does not enter argument for tor, it should be True by
        default."""
        options = dict(tor=True, full_scrapping=False)
        self.scrapper_cmd.handle(**options)
        result = self.scrapper_cmd.tor
        expected = True
        self.assertEqual(expected, result)

    def test_url1(self):
        """Test when user does not enter any argument for the scrapper."""
        options = dict(full_scrapping=False, tor=False)
        self.scrapper_cmd.handle(**options)
        expected = self.congreso_url
        self.assertEqual(expected, self.scrapper_cmd.urls[0])

    def test_url2(self):
        """Test when user enter argument for full scrapping, since 20110727."""
        options = dict(full_scrapping=True, tor=False)
        self.scrapper_cmd.handle(**options)
        expected_last = self.congreso_url + '&Start=3800'
        self.assertEqual(expected_last, self.scrapper_cmd.urls[-1])

    def test_get(self):
        soup = self.scrapper_cmd.get("http://www.bbc.com/news/")
        result = soup.title.get_text()
        expected = "BBC News - Home"
        self.assertEqual(result, expected)

    def test_extract_doc_links(self):
        expected = [
            {
            #'codigo': u'03774',
            'numero_proyecto': '03774/2014-CR',
            #'link': None,
            #'link_to_pdf': 'http://www2.congreso.gob.pe/sicr/tradocestproc/'
                           #'Expvirt_2011.nsf/visbusqptramdoc/03774?opendocument'
            #'pdf_url': 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/'
                       #'Contdoc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0'
                       #'dbc9030966aac60905257d4a007b75d9/$FILE
                       # /PL03774050914.pdf',
            'titulo': u'Propone establecer los lineamientos para la promoc'
                      u'i\xf3n de la eficiencia y competitividad en la '
                      u'actividad empresarial del Estado, garantizando su '
                      u'aporte estrat\xe9gico para el desarrollo'
                      u' descentralizado y la soberan\xeda nacional.',
            'seguimiento_page': 'http://www2.congreso.gob.pe/Sicr/TraDocEst'
                                'Proc/CLProLey2011.nsf/Sicr/TraDocEstProc/'
                                'CLProLey2011.nsf/PAporNumeroInverso/96091'
                                '30B9871582F05257D4A00752301?opendocument',
            }
        ]

        html_folder = os.path.abspath(os.path.dirname(__file__))
        html_file = os.path.join(html_folder, "frontweb.html")
        with codecs.open(html_file, "r", "utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html)
            our_links = self.scrapper_cmd.extract_doc_links(soup)
        self.assertEqual(expected, our_links)

    def test_extract_metadata1(self):
        obj = {'numero_proyecto': '03774/2014-CR', 'titulo': 'hola',
               'seguimiento_page': 'http://www2.congreso.gob.pe/Sicr/TraDocEst'
                                   'Proc/CLProLey2011.nsf/Sicr/TraDocEstProc/'
                                   'CLProLey2011.nsf/PAporNumeroInverso/96091'
                                   '30B9871582F05257D4A00752301?opendocument',
               }
        result = self.scrapper_cmd.extract_metadata(obj)
        expected = {
            'numero_proyecto': '03774/2014-CR',
            'codigo': '03774',
            'titulo': u'Propone establecer los lineamientos para la promoc'
                      u'i\xf3n de la eficiencia y competitividad en la '
                      u'actividad empresarial del Estado, garantizando su '
                      u'aporte estrat\xe9gico para el desarrollo'
                      u' descentralizado y la soberan\xeda nacional.',
            'fecha_presentacion': '05/09/2014',
            'link_to_pdf': 'http://www2.congreso.gob.pe/sicr/tradocestproc/'
                           'Expvirt_2011.nsf/visbusqptramdoc/03774?opendocu'
                           'ment',
        }
        self.assertEqual(expected, result)

    def test_extract_metadata2(self):
        obj = {'numero_proyecto': '03774/2014-CR', 'titulo': 'hola',
            'seguimiento_page': 'http://www2.congreso.gob.pe/Sicr/TraDocEst'
                                'Proc/CLProLey2011.nsf/Sicr/TraDocEstProc/'
                                'CLProLey2011.nsf/PAporNumeroInverso/96091'
                                '30B9871582F05257D4A00752301?opendocument',
            'fecha_presentacion': datetime.now()
        }
        b = Proyecto(numero_proyecto='03774/2014-CR', titulo='hola',
                     seguimiento_page=obj['seguimiento_page'],
                     fecha_presentacion=datetime.now())
        b.save()
        result = self.scrapper_cmd.extract_metadata(obj)
        self.assertEqual("already in database", result)

    def test_extract_pdf_url(self):
        link = 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011' \
               '.nsf/visbusqptramdoc/02764?opendocument'
        codigo = '02764'
        result = self.scrapper_cmd.extract_pdf_url(link, codigo)
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc0' \
                   '2_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/2a89be59a1' \
                   'a3966b05257c01000a5cd5/$FILE/PL02764101013.pdf'
        self.assertEqual(expected, result)

    def test_parse_names(self):
        congresistas = "Dammert Ego Aguirre  Manuel Enrique Ernesto,Lescano" \
                       " Ancieta  Yonhy,Merino De Lama  Manuel,Guevara " \
                       "Amasifuen  Mesias Antonio,Mavila Leon  Rosa Delsa," \
                       "Mendoza Frisch  Veronika Fanny"
        expected = "Dammert Ego Aguirre, Manuel Enrique Ernesto; Lescano " \
                   "Ancieta, Yonhy; Merino De Lama, Manuel; Guevara " \
                   "Amasifuen, Mesias Antonio; Mavila Leon, Rosa Delsa; " \
                   "Mendoza Frisch, Veronika Fanny"
        result = self.scrapper_cmd.parse_names(congresistas)
        self.assertEqual(expected, result)